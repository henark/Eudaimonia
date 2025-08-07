import { createMiddleware } from "@inlang/paraglide-js-adapter-next"
import type { NextRequest } from "next/server"

export const middleware = createMiddleware({
  exclude: ["/api/**"], // Exclude all API routes
})

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    "/((?!api|_next/static|_next/image|favicon.ico).*)",
  ],
}
