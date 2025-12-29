# Remaining Tasks - AURORA Tax Classifier

**Date**: December 29, 2024
**Status**: Backend Complete, Frontend Updates Pending

---

## ✅ Completed Tasks (This Session)

1. **Increased pagination limit** from 100 to 1000 rows ✅
2. **Added multi-sheet Excel support** - combines all sheets automatically ✅
3. **Removed scroll arrow** from landing page ✅
4. **Added amount/date column mapping** with intelligent field detection ✅
5. **Added total_amount** to job summary API ✅

---

## ⏳ Pending Frontend Tasks

### 1. Update Results Page - Display Amount and Tax Due Columns

**Location**: `frontend/src/pages/ResultsPage.tsx`

**Requirements**:
- Add `amount` column to the results table
- Add `tax_due` column (calculated as `amount * 0` for now since tax rate not specified)
- Format currency properly (Indonesian Rupiah format: `Rp 1.000.000,00`)

**Implementation Steps**:
```typescript
// Update the table headers
const columns = [
  "Row",
  "Account Name",
  "Tax Object",
  "Confidence",
  "Amount",        // NEW
  "Tax Due",       // NEW
  "Explanation"
];

// In the table body, add cells for amount and tax_due
<td className="px-6 py-4 text-sm text-gray-900">
  {row.amount ?
    new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency: 'IDR'
    }).format(row.amount)
    : '-'
  }
</td>
<td className="px-6 py-4 text-sm text-gray-900">
  Rp 0,00  {/* Placeholder until tax rates are configured */}
</td>
```

**Backend Support**: ✅ Already returns `amount` and `date` in row data

---

### 2. Add Total Amount to Tax Object Summary

**Location**: `frontend/src/pages/ResultsPage.tsx` - Summary section

**Requirements**:
- Display `total_amount` from the job summary API
- Format as Indonesian Rupiah
- Add to the existing summary cards

**Implementation**:
```typescript
// The API now returns summary.total_amount
const summary = job.summary;

// Add a new summary card
<div className="bg-white rounded-lg shadow p-6">
  <div className="flex items-center justify-between">
    <div>
      <p className="text-sm text-gray-600">Total Amount</p>
      <p className="text-2xl font-bold text-gray-900">
        {new Intl.NumberFormat('id-ID', {
          style: 'currency',
          currency: 'IDR',
          minimumFractionDigits: 0
        }).format(summary.total_amount || 0)}
      </p>
    </div>
    <div className="text-4xl">💰</div>
  </div>
</div>
```

**Backend Support**: ✅ API returns `summary.total_amount`

---

### 3. Add Date Range Filter/Slicer

**Location**: `frontend/src/pages/ResultsPage.tsx`

**Requirements**:
- Add date range picker above the results table
- Default range: January 1 - December 31 of current year
- Filter results based on the `date` field
- Update displayed rows and summary statistics based on filter

**Implementation Strategy**:

**Option A: Simple Date Inputs**
```typescript
const [startDate, setStartDate] = useState('2024-01-01');
const [endDate, setEndDate] = useState('2024-12-31');

const filteredRows = rows.filter(row => {
  if (!row.date) return true; // Include rows without dates
  const rowDate = new Date(row.date);
  return rowDate >= new Date(startDate) && rowDate <= new Date(endDate);
});

// UI
<div className="flex gap-4 mb-6">
  <div>
    <label>Start Date</label>
    <input
      type="date"
      value={startDate}
      onChange={(e) => setStartDate(e.target.value)}
      className="px-4 py-2 border rounded"
    />
  </div>
  <div>
    <label>End Date</label>
    <input
      type="date"
      value={endDate}
      onChange={(e) => setEndDate(e.target.value)}
      className="px-4 py-2 border rounded"
    />
  </div>
  <button onClick={applyFilter} className="px-6 py-2 bg-blue-500 text-white rounded">
    Apply Filter
  </button>
</div>
```

**Option B: shadcn/ui Calendar Component** (Recommended)
```bash
# Install the calendar component
npx shadcn@latest add calendar
npx shadcn@latest add popover
```

```typescript
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Button } from "@/components/ui/button"
import { CalendarIcon } from "lucide-react"

const [dateRange, setDateRange] = useState<DateRange | undefined>({
  from: new Date(2024, 0, 1),
  to: new Date(2024, 11, 31)
})
```

**Recalculate Summaries**:
```typescript
// After filtering, recalculate:
const filteredTotal = filteredRows.reduce((sum, row) =>
  sum + (row.amount || 0), 0
);

const filteredAvgConfidence = filteredRows.reduce((sum, row) =>
  sum + row.confidence_percent, 0
) / filteredRows.length;
```

**Backend Support**: ✅ Rows already include `date` field

---

### 4. Update Clerk Sign-In Page - Show Email/Password Form

**Location**: `frontend/src/pages/SignInPage.tsx`

**Current Issue**: Clerk's `<SignIn />` component shows the default UI which may not show email/password fields prominently.

**Solution**: Configure Clerk to show email/password form by default

**Implementation**:
```typescript
<SignIn
  appearance={{
    elements: {
      card: "bg-slate-800 shadow-2xl",
      formButtonPrimary: "bg-gradient-to-r from-blue-500 to-purple-600",
      // ... existing appearance config
    }
  }}
  routing="path"
  path="/sign-in"
  redirectUrl="/upload"
  signUpUrl="/sign-up"

  // Force email/password to show
  initialValues={{
    emailAddress: "",
  }}
/>
```

**Alternative**: If you want custom email/password fields instead of Clerk's component, you'll need to:
1. Use Clerk's `useSignIn()` hook
2. Build custom form with email and password inputs
3. Call `signIn.create()` manually

Example:
```typescript
import { useSignIn } from "@clerk/clerk-react";

const { signIn, setActive } = useSignIn();

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  try {
    const result = await signIn.create({
      identifier: email,
      password: password,
    });

    if (result.status === "complete") {
      await setActive({ session: result.createdSessionId });
      navigate("/upload");
    }
  } catch (err) {
    console.error("Error:", err);
  }
};
```

**Note**: The current Clerk implementation already works, this is just a UI preference change.

---

## 📊 Implementation Priority

### High Priority (Must Have)
1. ✅ Amount/Date column mapping (Backend) - **DONE**
2. ✅ Total amount in API (Backend) - **DONE**
3. ⏳ Display amount and tax_due columns in results table
4. ⏳ Display total_amount in summary section

### Medium Priority (Should Have)
5. ⏳ Date range filter with calendar picker
6. ⏳ Recalculate filtered summaries

### Low Priority (Nice to Have)
7. ⏳ Custom email/password form (current Clerk UI works fine)

---

## 🔧 Testing Checklist

### After Implementing Frontend Changes:

**Test Amount Display:**
- [ ] Upload a CSV with `amount` or `jumlah` column
- [ ] Verify amount appears in results table
- [ ] Verify amount is formatted as Indonesian Rupiah
- [ ] Verify tax_due column shows Rp 0,00
- [ ] Verify total_amount appears in summary card

**Test Date Filter:**
- [ ] Upload a CSV with `date` or `tanggal` column
- [ ] Verify date filter UI appears
- [ ] Select date range January-March
- [ ] Verify only rows in that range are shown
- [ ] Verify summary statistics update correctly
- [ ] Verify total_amount updates for filtered range

**Test Multi-Sheet Excel:**
- [ ] Upload an Excel file with multiple sheets
- [ ] Verify all sheets are processed
- [ ] Verify results include rows from all sheets
- [ ] Check that `sheet_name` column shows source sheet

**Test Large Files:**
- [ ] Upload a file with 1000+ rows
- [ ] Verify pagination shows all rows (up to 1000)
- [ ] Verify download includes all rows
- [ ] Verify performance is acceptable

---

## 📝 Code Templates

### Indonesian Rupiah Formatter (Reusable)

```typescript
// Create a utility function
export const formatRupiah = (amount: number | null | undefined): string => {
  if (amount === null || amount === undefined) return '-';

  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount);
};

// Usage
<td>{formatRupiah(row.amount)}</td>
```

### Date Formatter

```typescript
export const formatDate = (dateStr: string | null | undefined): string => {
  if (!dateStr) return '-';

  try {
    const date = new Date(dateStr);
    return new Intl.DateTimeFormat('id-ID', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    }).format(date);
  } catch {
    return dateStr; // Return as-is if invalid
  }
};

// Usage
<td>{formatDate(row.date)}</td>
```

---

## 🎯 Expected Final Result

After implementing all frontend changes:

**Results Table:**
```
| Row | Account Name      | Tax Object | Confidence | Amount          | Tax Due | Date          | Explanation |
|-----|-------------------|------------|------------|-----------------|---------|---------------|-------------|
| 1   | Gaji Karyawan    | PPh21      | 95%        | Rp 10.000.000   | Rp 0    | 15 Jan 2024   | Based on... |
| 2   | Biaya Sewa       | PPh4(2)    | 88%        | Rp 5.000.000    | Rp 0    | 20 Jan 2024   | Based on... |
```

**Summary Cards:**
```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ 📊 Total Rows   │  │ ✅ Avg Confidence│  │ ⚠️ Risk Level   │  │ 💰 Total Amount │
│ 1,000           │  │ 72.5%            │  │ 63.8%           │  │ Rp 150.000.000  │
└─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘
```

**Date Filter:**
```
┌─────────────────────────────────────────────────────────────┐
│ Filter by Date Range:                                       │
│ [📅 01 Jan 2024] to [📅 31 Dec 2024]  [Apply Filter]      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start for Next Session

```bash
# 1. Start servers (if not running)
cd backend && uvicorn src.main:app --reload
cd frontend && npm run dev

# 2. Install calendar components (for date filter)
cd frontend
npx shadcn@latest add calendar
npx shadcn@latest add popover

# 3. Edit ResultsPage.tsx
code frontend/src/pages/ResultsPage.tsx

# 4. Test with sample file that has amount and date columns
```

---

**Document Created**: December 29, 2024, 04:15 AM
**Backend Status**: ✅ Complete
**Frontend Status**: ⏳ Awaiting Implementation
