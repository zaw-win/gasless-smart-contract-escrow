import { useRouter } from 'next/router';
import CreateInvoiceForm from '@/components/CreateInvoiceForm';
import { createInvoice } from '@/services/api';

export default function CreateInvoicePage() {
  const router = useRouter();

  async function handleCreate(client: string, freelancer: string, amounts: number[]) {
    const { invoice_id } = await createInvoice(client, freelancer, amounts);
    router.push(`/invoices/${invoice_id}`);
  }

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Create New Invoice</h1>
      <CreateInvoiceForm onSubmit={handleCreate} />
    </div>
  );
}