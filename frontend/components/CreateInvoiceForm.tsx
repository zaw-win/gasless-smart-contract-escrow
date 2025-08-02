import { useState, FormEvent } from 'react';
import { useSession } from 'next-auth/react';
import React from 'react';

interface Props {
  onSubmit: (client:string, freelancer: string, amounts: number[]) => void;
}

export default function CreateInvoiceForm({ onSubmit }: Props) {
  const { data: session } = useSession();
  const [client, setClient] = useState(session?.user?.email || '');
  const [freelancer, setFreelancer] = useState('');
  const [amountsText, setAmountsText] = useState('');
  const [error, setError] = useState<string | null>(null);

  // If session changes (e.g., after login), update client
  React.useEffect(() => {
    if (session?.user?.email) setClient(session.user.email);
  }, [session]);

  function parseAmounts(text: string): number[] {
    return text
      .split(',')
      .map((s) => parseFloat(s.trim())) // USDC 6 decimals
      .filter((n) => !isNaN(n));
  }

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const amounts = parseAmounts(amountsText);
    if (!client || !freelancer || amounts.length === 0) {
      setError('Please enter a valid client, freelancer and comma-separated amounts.');
      return;
    }
    onSubmit(client, freelancer, amounts);
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <div className="text-red-600">{error}</div>}
      <div>
        <label className="block text-sm">Client Email</label>
        <input
          type="text"
          value={client}
          onChange={(e) => setClient(e.target.value)}
          className="w-full border rounded p-2"
          placeholder="0x..."
          readOnly // Make the client field read-only
        />
      </div>
      <div>
        <label className="block text-sm">Freelancer Email</label>
        <input
          type="text"
          value={freelancer}
          onChange={(e) => setFreelancer(e.target.value)}
          className="w-full border rounded p-2"
          placeholder="0x..."
        />
      </div>
      <div>
        <label className="block text-sm">
          Milestone Amounts (comma-separated USDC)
        </label>
        <input
          type="text"
          value={amountsText}
          onChange={(e) => setAmountsText(e.target.value)}
          className="w-full border rounded p-2"
          placeholder="50, 100, 150"
        />
      </div>
      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        Create Invoice
      </button>
    </form>
  );
}