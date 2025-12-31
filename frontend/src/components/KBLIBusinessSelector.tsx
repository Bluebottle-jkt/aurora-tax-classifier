import { useState, useEffect } from 'react';
import api from '../lib/axios';
import { motion, AnimatePresence } from 'framer-motion';

interface Division {
  code: string;
  name: string;
  keywords: string[];
}

interface Category {
  code: string;
  name: string;
  divisions: Division[];
}

interface KBLIData {
  metadata: {
    source: string;
    level: string;
    notes: string[];
  };
  categories: Category[];
}

interface KBLIBusinessSelectorProps {
  onSelectionChange: (selectedCategories: string[], selectedDivisions: string[]) => void;
  selectedCategories?: string[];
  selectedDivisions?: string[];
}

export default function KBLIBusinessSelector({
  onSelectionChange,
  selectedCategories = [],
  selectedDivisions = []
}: KBLIBusinessSelectorProps) {
  const [kbliData, setKbliData] = useState<KBLIData | null>(null);
  const [loading, setLoading] = useState(true);
  const [internalSelectedCategories, setInternalSelectedCategories] = useState<string[]>(selectedCategories);
  const [internalSelectedDivisions, setInternalSelectedDivisions] = useState<string[]>(selectedDivisions);

  useEffect(() => {
    loadKBLIData();
  }, []);

  const loadKBLIData = async () => {
    try {
      const response = await api.get('/api/kbli/categories');
      setKbliData(response.data);
    } catch (error) {
      console.error('Failed to load KBLI data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCategoryToggle = (categoryCode: string) => {
    const newSelectedCategories = internalSelectedCategories.includes(categoryCode)
      ? internalSelectedCategories.filter(c => c !== categoryCode)
      : [...internalSelectedCategories, categoryCode];

    setInternalSelectedCategories(newSelectedCategories);

    // If deselecting a category, also remove its divisions
    if (!newSelectedCategories.includes(categoryCode)) {
      const category = kbliData?.categories.find(c => c.code === categoryCode);
      const divisionCodesToRemove = category?.divisions.map(d => d.code) || [];
      const newSelectedDivisions = internalSelectedDivisions.filter(
        d => !divisionCodesToRemove.includes(d)
      );
      setInternalSelectedDivisions(newSelectedDivisions);
      onSelectionChange(newSelectedCategories, newSelectedDivisions);
    } else {
      onSelectionChange(newSelectedCategories, internalSelectedDivisions);
    }
  };

  const handleDivisionToggle = (divisionCode: string) => {
    const newSelectedDivisions = internalSelectedDivisions.includes(divisionCode)
      ? internalSelectedDivisions.filter(d => d !== divisionCode)
      : [...internalSelectedDivisions, divisionCode];

    setInternalSelectedDivisions(newSelectedDivisions);
    onSelectionChange(internalSelectedCategories, newSelectedDivisions);
  };

  const getAvailableDivisions = () => {
    if (!kbliData) return [];

    const divisions: Division[] = [];
    kbliData.categories.forEach(category => {
      if (internalSelectedCategories.includes(category.code)) {
        divisions.push(...category.divisions);
      }
    });
    return divisions;
  };

  if (loading) {
    return (
      <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
        <div className="flex items-center justify-center gap-3">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-indigo-600"></div>
          <p className="text-gray-600">Loading business categories...</p>
        </div>
      </div>
    );
  }

  if (!kbliData) {
    return (
      <div className="bg-red-50 rounded-lg p-4 border border-red-200">
        <p className="text-red-600">Failed to load business categories. Please refresh the page.</p>
      </div>
    );
  }

  const availableDivisions = getAvailableDivisions();

  return (
    <div className="space-y-6">
      {/* Step 1: General Category Selection */}
      <div className="bg-white rounded-xl border-2 border-indigo-200 p-6">
        <h3 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
          <span className="bg-indigo-600 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm">1</span>
          Select General Business Categories (One or More)
        </h3>
        <p className="text-sm text-gray-600 mb-4">
          Choose the general industry categories that apply to your business
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 max-h-[400px] overflow-y-auto pr-2">
          {kbliData.categories.map((category) => {
            const isSelected = internalSelectedCategories.includes(category.code);
            return (
              <motion.div
                key={category.code}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => handleCategoryToggle(category.code)}
                className={`cursor-pointer rounded-lg p-4 border-2 transition-all ${
                  isSelected
                    ? 'border-indigo-600 bg-indigo-50 shadow-md'
                    : 'border-gray-200 bg-white hover:border-indigo-300 hover:shadow-sm'
                }`}
              >
                <div className="flex items-start gap-3">
                  <div className={`flex-shrink-0 w-6 h-6 rounded border-2 flex items-center justify-center ${
                    isSelected ? 'bg-indigo-600 border-indigo-600' : 'border-gray-300'
                  }`}>
                    {isSelected && (
                      <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <h4 className="font-bold text-gray-800 text-sm mb-1">
                      {category.code}. {category.name}
                    </h4>
                    <p className="text-xs text-gray-500">
                      {category.divisions.length} sub-categories
                    </p>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* Step 2: Specific Business Type Selection */}
      <AnimatePresence>
        {internalSelectedCategories.length > 0 && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="bg-white rounded-xl border-2 border-purple-200 p-6"
          >
            <h3 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
              <span className="bg-purple-600 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm">2</span>
              Select Specific Business Types (One or More)
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              Choose specific business activities from the selected categories
            </p>

            {availableDivisions.length === 0 ? (
              <div className="bg-yellow-50 rounded-lg p-4 border border-yellow-200">
                <p className="text-yellow-800 text-sm">
                  Please select at least one general category above to see specific business types.
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 gap-3 max-h-[500px] overflow-y-auto pr-2">
                {availableDivisions.map((division) => {
                  const isSelected = internalSelectedDivisions.includes(division.code);
                  const parentCategory = kbliData.categories.find(c =>
                    c.divisions.some(d => d.code === division.code)
                  );

                  return (
                    <motion.div
                      key={division.code}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      whileHover={{ scale: 1.01 }}
                      whileTap={{ scale: 0.99 }}
                      onClick={() => handleDivisionToggle(division.code)}
                      className={`cursor-pointer rounded-lg p-4 border-2 transition-all ${
                        isSelected
                          ? 'border-purple-600 bg-purple-50 shadow-md'
                          : 'border-gray-200 bg-white hover:border-purple-300 hover:shadow-sm'
                      }`}
                    >
                      <div className="flex items-start gap-3">
                        <div className={`flex-shrink-0 w-6 h-6 rounded border-2 flex items-center justify-center ${
                          isSelected ? 'bg-purple-600 border-purple-600' : 'border-gray-300'
                        }`}>
                          {isSelected && (
                            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                            </svg>
                          )}
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="text-xs font-semibold text-indigo-600 bg-indigo-100 px-2 py-0.5 rounded">
                              {parentCategory?.code}
                            </span>
                            <span className="text-xs font-semibold text-purple-600 bg-purple-100 px-2 py-0.5 rounded">
                              {division.code}
                            </span>
                          </div>
                          <h4 className="font-bold text-gray-800 text-sm mb-2">
                            {division.name}
                          </h4>
                          <div className="flex flex-wrap gap-1">
                            {division.keywords.slice(0, 5).map((keyword, idx) => (
                              <span key={idx} className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded">
                                {keyword}
                              </span>
                            ))}
                            {division.keywords.length > 5 && (
                              <span className="text-xs text-gray-500">
                                +{division.keywords.length - 5} more
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Selection Summary */}
      {(internalSelectedCategories.length > 0 || internalSelectedDivisions.length > 0) && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="bg-green-50 rounded-lg p-4 border border-green-200"
        >
          <h4 className="font-bold text-green-800 mb-2 flex items-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Selection Summary
          </h4>
          <div className="space-y-1 text-sm text-green-700">
            <p>
              <span className="font-semibold">{internalSelectedCategories.length}</span> general {internalSelectedCategories.length === 1 ? 'category' : 'categories'} selected
            </p>
            <p>
              <span className="font-semibold">{internalSelectedDivisions.length}</span> specific business {internalSelectedDivisions.length === 1 ? 'type' : 'types'} selected
            </p>
          </div>
        </motion.div>
      )}
    </div>
  );
}
