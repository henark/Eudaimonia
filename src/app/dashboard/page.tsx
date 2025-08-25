'use client'

import { useSession, signOut } from "next-auth/react"
import { useRouter } from "next/navigation"

export default function DashboardPage() {
  const { data: session, status } = useSession()
  const router = useRouter()

  if (status === "loading") {
    return <p>Loading...</p>
  }

  if (status === "unauthenticated") {
    router.push("/auth/signin")
    return null
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {session?.user?.name || session?.user?.email}!</p>
      <pre>{JSON.stringify(session, null, 2)}</pre>
      <button onClick={() => signOut({ callbackUrl: '/' })}>Sign Out</button>
    </div>
  )
}
