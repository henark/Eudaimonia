'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useQuery } from 'react-query'
import axios from 'axios'

interface LivingWorld {
  id: string
  name: string
  description: string
  member_count: number
  theme_data: any
}

interface Post {
  id: string
  content: string
  author: {
    username: string
  }
  world: {
    name: string
  }
  created_at: string
}

interface SmartProfile {
  id: string
  name: string
  did: string
}

export default function Dashboard() {
  const [userProfile, setUserProfile] = useState<any>(null)

  // Fetch user's LivingWorlds
  const { data: worlds, isLoading: worldsLoading } = useQuery(
    'userWorlds',
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
        console.error('Error fetching worlds:', error)
      }
    }
  )

  // Fetch recent posts
  const { data: posts, isLoading: postsLoading } = useQuery(
    'recentPosts',
    async () => {
      const token = localStorage.getItem('authToken')
      const response = await axios.get('/api/posts/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data.results || response.data
    },
    {
      retry: false,
      onError: (error) => {
        console.error('Error fetching posts:', error)
      }
    }
  )

  // Fetch Smart Profiles
  const { data: smartProfiles, isLoading: profilesLoading } = useQuery(
    'smartProfiles',
    async () => {
      const token = localStorage.getItem('authToken')
      const response = await axios.get('/api/smart-profiles/', {
        headers: { Authorization: `Bearer ${token}` },
      })
      return response.data.results || response.data
    },
    {
      retry: false,
      onError: (error) => {
        console.error('Error fetching smart profiles:', error)
      },
    }
  )

  useEffect(() => {
    // Fetch user profile
    const fetchProfile = async () => {
      try {
        const token = localStorage.getItem('authToken')
        const response = await axios.get('/api/me/profile/', {
          headers: { Authorization: `Bearer ${token}` }
        })
        setUserProfile(response.data)
      } catch (error) {
        console.error('Error fetching profile:', error)
      }
    }
    fetchProfile()
  }, [])

  return (
    <div className="max-w-7xl mx-auto">
      {/* Welcome Section */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Welcome back, {userProfile?.username || 'User'}!
        </h1>
        <p className="text-gray-600">
          Explore your Living Worlds and connect with your communities.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Your Smart Profiles */}
        <div className="lg:col-span-1 bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">Your Smart Profiles</h2>
            <Link
              href="/dashboard/profiles"
              className="text-primary-600 hover:text-primary-700 text-sm font-medium"
            >
              Manage
            </Link>
          </div>

          {profilesLoading ? (
            <div className="animate-pulse space-y-3">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-12 bg-gray-200 rounded"></div>
              ))}
            </div>
          ) : smartProfiles && smartProfiles.length > 0 ? (
            <div className="space-y-3">
              {smartProfiles.slice(0, 4).map((profile: SmartProfile) => (
                <div key={profile.id} className="p-3 border border-gray-200 rounded-lg">
                  <p className="font-medium text-gray-900">{profile.name}</p>
                  <p className="text-sm text-gray-500 truncate">{profile.did || 'No DID yet'}</p>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <p className="text-gray-500 mb-4">You have no Smart Profiles.</p>
              <Link
                href="/dashboard/profiles"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
              >
                Create a Profile
              </Link>
            </div>
          )}
        </div>

        <div className="lg:col-span-2 grid grid-cols-1 gap-6">
          {/* Your Living Worlds */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Your Living Worlds</h2>
              <Link
                href="/dashboard/worlds"
                className="text-primary-600 hover:text-primary-700 text-sm font-medium"
              >
                View all
              </Link>
            </div>

            {worldsLoading ? (
              <div className="animate-pulse space-y-3">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="h-16 bg-gray-200 rounded"></div>
                ))}
              </div>
            ) : userProfile && userProfile.community_memberships.length > 0 ? (
              <div className="space-y-3">
                {userProfile.community_memberships.slice(0, 3).map((membership: any) => (
                  <Link
                    key={membership.world_name}
                    href={`/dashboard/worlds/${membership.world_id}`}
                    className="block p-3 border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-medium text-gray-900">{membership.world_name}</h3>
                        <p className="text-sm text-gray-500">{membership.profile_name} - {membership.role}</p>
                      </div>
                      <div className="text-right">
                        <span className="text-sm text-gray-500">{membership.reputation} rep</span>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-gray-500 mb-4">You haven't joined any Living Worlds yet.</p>
                <Link
                  href="/dashboard/worlds"
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
                >
                  Discover Worlds
                </Link>
              </div>
            )}
          </div>

          {/* Recent Activity */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">Recent Activity</h2>
            <Link
              href="/dashboard/activity"
              className="text-primary-600 hover:text-primary-700 text-sm font-medium"
            >
              View all
            </Link>
          </div>
          
          {postsLoading ? (
            <div className="animate-pulse space-y-3">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-16 bg-gray-200 rounded"></div>
              ))}
            </div>
          ) : posts && posts.length > 0 ? (
            <div className="space-y-3">
              {posts.slice(0, 3).map((post: Post) => (
                <div key={post.id} className="p-3 border border-gray-200 rounded-lg">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <p className="text-sm text-gray-900 line-clamp-2">{post.content}</p>
                      <div className="flex items-center mt-2 text-xs text-gray-500">
                        <span>{post.author.username}</span>
                        <span className="mx-1">•</span>
                        <span>{post.world.name}</span>
                        <span className="mx-1">•</span>
                        <span>{new Date(post.created_at).toLocaleDateString()}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <p className="text-gray-500">No recent activity.</p>
            </div>
          )}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mt-6 bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link
            href="/dashboard/worlds/create"
            className="flex items-center p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors"
          >
            <div className="flex-shrink-0">
              <svg className="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-gray-900">Create World</h3>
              <p className="text-sm text-gray-500">Start a new community</p>
            </div>
          </Link>

          <Link
            href="/dashboard/friends"
            className="flex items-center p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors"
          >
            <div className="flex-shrink-0">
              <svg className="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-gray-900">Friends</h3>
              <p className="text-sm text-gray-500">Manage connections</p>
            </div>
          </Link>

          <Link
            href="/dashboard/companion"
            className="flex items-center p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors"
          >
            <div className="flex-shrink-0">
              <svg className="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-gray-900">AI Companion</h3>
              <p className="text-sm text-gray-500">Get personalized help</p>
            </div>
          </Link>
        </div>
      </div>
    </div>
  )
} 