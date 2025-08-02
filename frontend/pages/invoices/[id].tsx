import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import MilestoneItem from '@/components/MilestoneItem';
import { fetchInvoice } from '@/services/api';

export default function InvoiceDetail() {
  const router = useRouter();
  const { id } = router.query;
  const [invoice, setInvoice] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function loadInvoice() {
    if (!id) return;
    setLoading(true);
    try {
      const data = await fetchInvoice(Number(id));
      setInvoice(data);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { loadInvoice(); }, [id]);

  if (loading) return <div>Loading invoice…</div>;
  if (error) return <div className="text-red-600">Error: {error}</div>;

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl font-bold">Invoice #{invoice.invoice_id}</h1>
      <div>Client: {invoice.client_email}</div>
      <div>Freelancer: {invoice.freelancer_email}</div>
      <div className="mt-4">
        <h2 className="font-semibold">Milestones</h2>
        <div className="space-y-2">
          {invoice.milestones.map((m: any) => (
            <MilestoneItem
              key={m.index}
              invoiceId={invoice.invoice_id}
              index={m.index}
              amount={m.amount}
              funded={m.funded}
              released={m.released}
              onStatusChange={loadInvoice}
            />
          ))}
        </div>
      </div>
    </div>
  );
}