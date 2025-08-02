import Link from 'next/link';

interface Props {
  invoice: {
    invoice_id: number;
    freelancer: string;
    milestones: { funded: boolean; released: boolean }[];
  };
}

export default function InvoiceCard({ invoice }: Props) {
  const fundedCount = invoice.milestones.filter((m) => m.funded).length;
  const total = invoice.milestones.length;

  return (
    <Link href={`/invoices/${invoice.invoice_id}`}>
      <a className="block p-4 border rounded hover:bg-gray-50">
        <div className="flex justify-between">
          <div>Invoice #{invoice.invoice_id}</div>
          <div>{fundedCount}/{total} funded</div>
        </div>
        <div className="text-sm text-gray-600">
          Freelancer: {invoice.freelancer}
        </div>
      </a>
    </Link>
  );
}