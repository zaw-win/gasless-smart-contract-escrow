"use client";
import { useSession, signIn, signOut } from 'next-auth/react';

export default function NavBar() {
  const { data: session } = useSession();
  return (
    <nav className="p-4 flex justify-between bg-white shadow">
      <div className="font-bold">Escrow POC</div>
      <div>
        {session ? (
          <button onClick={() => signOut()} className="btn-red">Sign out</button>
        ) : (
          <button onClick={() => signIn('google')} className="btn-blue">
            Sign in with Google
          </button>
        )}
      </div>
    </nav>
  );
}