import NextAuth from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import jwt, { SignOptions } from "jsonwebtoken";

const NEXTAUTH_SECRET = process.env.NEXTAUTH_SECRET || "my-super-random-secret-string-not-32-bytes";
if (!NEXTAUTH_SECRET) throw new Error("Missing NEXTAUTH_SECRET");

function encode({ token = {}, secret = NEXTAUTH_SECRET }: { token?: any; secret?: string | Buffer }) {
  // Remove exp if present to avoid conflict
  const { exp, ...tokenWithoutExp } = token;
  const options: SignOptions = {
    algorithm: "HS256",
    // No expiresIn here
  };
  return jwt.sign(tokenWithoutExp, secret, options);
}

function decode({ token, secret = NEXTAUTH_SECRET }: { token?: string; secret?: string | Buffer }) {
  if (!token) return null;
  try {
    return jwt.verify(token, secret, { algorithms: ["HS256"] }) as any;
  } catch {
    return null;
  }
}

export default NextAuth({
  session: { strategy: "jwt" },
  secret: NEXTAUTH_SECRET,
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  jwt: {
    encode,
    decode,
  },
  callbacks: {
    async jwt({ token, account, profile }) {
      if (account && profile) {
        token.email = profile.email;
        
        // Check if user exists in database and create if not
        try {
          await fetch(`${process.env.NEXT_PUBLIC_API_URL}/user/status`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              email: profile.email
            }),
          });
        } catch (error) {
          console.error('Error checking/creating user:', error);
        }
      }
      return token;
    },
    async session({ session, token }) {
      session.user = { 
        email: token.email as string
      };
      return session;
    },
  },
});