'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useQuery } from 'react-query'
import axios from 'axios'

interface LivingWorld {
  id: string
  name: string
  description: string
  theme_data: any
}

interface Membership {
  id: string
  world: LivingWorld
  role: string
  reputation: number
}

export default function Sidebar() {
  const pathname = usePathname()
  const [isCollapsed, setIsCollapsed] = useState(false)

  // Fetch user's LivingWorlds
  const { data: memberships, isLoading } = useQuery(
    'userMemberships',
    async () => {
      const token = localStorage.getItem('authToken')
      const response = await axios.get('/api/memberships/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data.results || response.data
    },
    {
      retry: false,
      onError: (error) => {
        console.error('Error fetching memberships:', error)
      }
    }
  )

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: 'HomeIcon' },
    { name: 'Living Worlds', href: '/dashboard/worlds', icon: 'GlobeIcon' },
    { name: 'Friends', href: '/dashboard/friends', icon: 'UsersIcon' },
    { name: 'AI Companion', href: '/dashboard/companion', icon: 'ChatIcon' },
  ]

  const renderIcon = (iconName: string) => {
    switch (iconName) {
      case 'HomeIcon':
        return (
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
        )
      case 'GlobeIcon':
        return (
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        )
      case 'UsersIcon':
        return (
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
          </svg>
        )
      case 'ChatIcon':
        return (
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        )
      default:
        return null
    }
  }

  return (
    <div className={`bg-white shadow-lg ${isCollapsed ? 'w-16' : 'w-64'} transition-all duration-300`}>
      <div className="flex flex-col h-full">
        {/* Toggle button */}
        <div className="flex justify-end p-4">
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="p-2 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100"
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>

        {/* Main Navigation */}
        <nav className="flex-1 px-2 space-y-1">
          {navigation.map((item) => {
            const isActive = pathname === item.href
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                  isActive
                    ? 'bg-primary-100 text-primary-900'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                }`}
              >
                {renderIcon(item.icon)}
                {!isCollapsed && <span className="ml-3">{item.name}</span>}
              </Link>
            )
          })}
        </nav>

        {/* Living Worlds Section */}
        <div className="border-t border-gray-200 p-4">
          {!isCollapsed && (
            <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
              Your Worlds
            </h3>
          )}
          
          {isLoading ? (
            <div className="space-y-2">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-8 bg-gray-200 rounded animate-pulse"></div>
              ))}
            </div>
          ) : memberships && memberships.length > 0 ? (
            <div className="space-y-1">
              {memberships.map((membership: Membership) => {
                const isActive = pathname === `/dashboard/worlds/${membership.world.id}`
                return (
                  <Link
                    key={membership.id}
                    href={`/dashboard/worlds/${membership.world.id}`}
                    className={`group flex items-center px-2 py-2 text-sm rounded-md ${
                      isActive
                        ? 'bg-primary-100 text-primary-900'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                    title={isCollapsed ? membership.world.name : undefined}
                  >
                    <div className="flex-shrink-0 w-6 h-6 rounded-full bg-primary-200 flex items-center justify-center">
                      <span className="text-xs font-medium text-primary-800">
                        {membership.world.name.charAt(0).toUpperCase()}
                      </span>
                    </div>
                    {!isCollapsed && (
                      <div className="ml-3 flex-1 min-w-0">
                        <p className="text-sm font-medium truncate">{membership.world.name}</p>
                        <p className="text-xs text-gray-500">{membership.role}</p>
                      </div>
                    )}
                  </Link>
                )
              })}
            </div>
          ) : (
            !isCollapsed && (
              <div className="text-center">
                <p className="text-xs text-gray-500">No worlds yet</p>
                <Link
                  href="/dashboard/worlds"
                  className="text-xs text-primary-600 hover:text-primary-700"
                >
                  Discover worlds
                </Link>
              </div>
            )
          )}
        </div>
      </div>
    </div>
  )
} 