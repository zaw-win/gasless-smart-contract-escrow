import { useState } from 'react';
import { fundMilestone, releaseMilestone } from '@/services/api';

interface Props {
  invoiceId: number;
  index: number;
  amount: number;
  funded: boolean;
  released: boolean;
  onStatusChange: () => void;
}

export default function MilestoneItem({
  invoiceId,
  index,
  amount,
  funded,
  released,
  onStatusChange,
}: Props) {
  const [loading, setLoading] = useState(false);

  async function handleFund() {
    setLoading(true);
    try {
      await fundMilestone(invoiceId, index);
      onStatusChange();
    } finally {
      setLoading(false);
    }
  }

  async function handleRelease() {
    setLoading(true);
    try {
      await releaseMilestone(invoiceId, index);
      onStatusChange();
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex items-center justify-between p-2 border rounded">
      <div>
        <div className="font-medium">Milestone {index}</div>
        <div className="text-sm">{amount} USDC</div>
        <div className="text-xs text-gray-600">
          {funded ? 'Funded' : 'Not Funded'} — {released ? 'Released' : 'Locked'}
        </div>
      </div>
      <div className="flex space-x-2">
        {!funded && (
          <button
            onClick={handleFund}
            disabled={loading}
            className="px-3 py-1 bg-green-600 text-white rounded"
          >
            {loading ? 'Funding…' : 'Fund'}
          </button>
        )}
        {funded && !released && (
          <button
            onClick={handleRelease}
            disabled={loading}
            className="px-3 py-1 bg-blue-600 text-white rounded"
          >
            {loading ? 'Releasing…' : 'Release'}
          </button>
        )}
      </div>
    </div>
  );
}