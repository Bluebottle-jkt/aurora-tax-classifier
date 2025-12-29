"""
Process Job Use Case - Core classification logic
"""

import pandas as pd
from typing import List, Dict, Any
from datetime import datetime
from ...domain.entities import (
    Job, PredictionRow, RiskReport, AuditTrail, JobStatus
)
from ...domain.value_objects import TaxObjectLabel, ConfidenceScore, RiskScore
from ...domain.policies import ConfidencePolicy, RiskPolicy
from ..ports import (
    JobRepositoryPort, PredictionRepositoryPort,
    ClassifierPort, StoragePort, ConfigPort, ExplainabilityPort
)


class ProcessJobUseCase:
    """Processes a classification job"""

    def __init__(
        self,
        job_repository: JobRepositoryPort,
        prediction_repository: PredictionRepositoryPort,
        classifier: ClassifierPort,
        storage: StoragePort,
        config: ConfigPort,
        explainer: ExplainabilityPort,
        confidence_policy: ConfidencePolicy,
        risk_policy: RiskPolicy,
    ):
        self.job_repo = job_repository
        self.pred_repo = prediction_repository
        self.classifier = classifier
        self.storage = storage
        self.config = config
        self.explainer = explainer
        self.confidence_policy = confidence_policy
        self.risk_policy = risk_policy

    def execute(self, job_id: str) -> None:
        """Process a job"""
        # Get job
        job = self.job_repo.find_by_id(job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")

        try:
            # Start processing
            job.start_processing()
            self.job_repo.save(job)

            # Load data
            file_path = self.storage.get_file_path(job_id, job.file_name)
            df = self._load_data(file_path)

            # Validate required columns
            if 'account_name' not in df.columns:
                raise ValueError("Missing required column: account_name")

            # Classify
            texts = df['account_name'].fillna("").astype(str).tolist()
            predictions = self.classifier.predict_proba(texts)

            # Create prediction rows
            rows = self._create_prediction_rows(
                job_id, df, predictions
            )

            # Save predictions
            self.pred_repo.save_batch(rows)

            # Calculate risk
            risk_report = self._calculate_risk(job, rows, df)

            # Calculate summary
            avg_confidence = sum(r.confidence.score for r in rows) / len(rows)

            # Mark completed
            job.mark_completed(
                total_rows=len(rows),
                avg_confidence=avg_confidence,
                risk_percent=risk_report.risk_score.score,
            )
            self.job_repo.save(job)

        except Exception as e:
            job.mark_failed(str(e))
            self.job_repo.save(job)
            raise

    def _load_data(self, file_path: str) -> pd.DataFrame:
        """Load CSV or Excel file"""
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding='utf-8')
        else:
            # Read Excel file - handle multi-sheet files
            excel_file = pd.ExcelFile(file_path)

            # If multiple sheets, read all and combine
            if len(excel_file.sheet_names) > 1:
                dfs = []
                for sheet_name in excel_file.sheet_names:
                    sheet_df = pd.read_excel(excel_file, sheet_name=sheet_name)
                    sheet_df['sheet_name'] = sheet_name  # Track source sheet
                    dfs.append(sheet_df)
                df = pd.concat(dfs, ignore_index=True)
            else:
                # Single sheet - read directly
                df = pd.read_excel(file_path)

        # Map common column names to account_name if missing
        if 'account_name' not in df.columns:
            for col in ['description', 'account_description', 'nama_akun', 'deskripsi']:
                if col in df.columns:
                    df['account_name'] = df[col]
                    break

        return df

    def _create_prediction_rows(
        self, job_id: str, df: pd.DataFrame, predictions: List[Dict[str, float]]
    ) -> List[PredictionRow]:
        """Create prediction row entities"""
        rows = []

        for idx, (_, row_data) in enumerate(df.iterrows()):
            prob_dist = predictions[idx]
            account_name = str(row_data.get('account_name', ''))

            # Get predicted label
            predicted_label_str = max(prob_dist, key=prob_dist.get)
            predicted_label = TaxObjectLabel(predicted_label_str)

            # Calculate confidence
            confidence, signals = self.confidence_policy.calculate(
                prob_dist, account_name
            )

            # Get explanation
            top_terms = self.explainer.get_top_terms(
                account_name, predicted_label_str
            )
            explanation = f"Based on terms: {', '.join(top_terms[:3])}"

            # Create row
            pred_row = PredictionRow(
                row_id=f"{job_id}_row_{idx}",
                job_id=job_id,
                row_index=idx,
                account_name=account_name,
                predicted_label=predicted_label,
                confidence=confidence,
                explanation=explanation,
                signals=signals,
                account_code=row_data.get('account_code'),
                amount=row_data.get('amount'),
                date=str(row_data.get('date')) if pd.notna(row_data.get('date')) else None,
                probability_distribution=prob_dist,
                top_terms=top_terms,
            )
            rows.append(pred_row)

        return rows

    def _calculate_risk(
        self, job: Job, rows: List[PredictionRow], df: pd.DataFrame
    ) -> RiskReport:
        """Calculate risk report"""
        # Get expected priors
        priors = self.config.get_priors()
        expected_dist = priors.get(job.business_type, priors.get("Default", {}))

        # Calculate observed distribution
        label_counts = {}
        total_weight = 0.0

        for row in rows:
            label = str(row.predicted_label)
            weight = abs(row.amount) if row.amount else 1.0
            weight *= row.confidence.score / 100.0

            label_counts[label] = label_counts.get(label, 0) + 1
            total_weight += weight

        # Normalize to distribution
        observed_dist = {
            label: (count / len(rows)) for label, count in label_counts.items()
        }

        # Calculate risk
        risk_score, anomaly_components, distance, anomaly =             self.risk_policy.calculate(
                observed_dist, expected_dist, label_counts, len(rows)
            )

        return RiskReport(
            job_id=job.job_id,
            business_type=job.business_type,
            risk_score=risk_score,
            label_distribution=observed_dist,
            expected_distribution=expected_dist,
            distribution_distance=distance,
            anomaly_score=anomaly,
            anomaly_components=anomaly_components,
            quality_warnings=[],
            metadata={},
        )
