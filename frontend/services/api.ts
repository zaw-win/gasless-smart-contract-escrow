const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function fetchWithAuth(input: RequestInfo, init: RequestInit = {}) {
  const res = await fetch(input.toString(), {
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...init.headers },
    ...init,
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function createInvoice(client: string, freelancer: string, milestone_amounts: number[]) {
  return fetchWithAuth(`${API_URL}/invoice`, {
    method: 'POST',
    body: JSON.stringify({ 
      client_email: client, 
      freelancer_email: freelancer, 
      milestone_amounts: milestone_amounts 
    }),
  });
}

export async function fetchInvoice(id: number) {
  return fetchWithAuth(`${API_URL}/invoice/${id}`);
}

export async function fundMilestone(invoice_id: number, index: number) {
  return fetchWithAuth(
    `${API_URL}/escrow/fund`,
    {
      method: 'POST',
      body: JSON.stringify({ invoice_id, index }),
    }
  );
}

export async function releaseMilestone(invoice_id: number, index: number) {
  return fetchWithAuth(
    `${API_URL}/escrow/release`,
    {
      method: 'POST',
      body: JSON.stringify({ invoice_id, index }),
    }
  );
}