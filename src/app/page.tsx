'use client'

import { useSession } from "next-auth/react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { useEffect } from "react"

export default function HomePage() {
  const { data: session, status } = useSession()
  const router = useRouter()

  useEffect(() => {
    if (status === "authenticated") {
      router.push("/dashboard")
    }
  }, [status, router])

  if (status === "loading") {
    return <p>Loading...</p>
  }

  return (
    <div>
      <h1>Welcome to Eudaimonia</h1>
      <p>Please sign in to continue.</p>
      <Link href="/auth/signin">Sign In</Link>
    </div>
  )
}
