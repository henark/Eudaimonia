'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import axios from 'axios'
import CreatePostForm from '@/components/CreatePostForm'

interface LivingWorld {
  id: string
  name: string
  description: string
  theme_data: {
    backgroundColor?: string
    primaryColor?: string
    secondaryColor?: string
  }
  owner: {
    username: string
  }
  member_count: number
}

interface Post {
  id: string
  content: string
  author: {
    username: string
  }
  created_at: string
}

interface Member {
  id: string
  profile: {
    name: string
    user: {
      username: string
    }
  }
  role: string
  reputation: number
  joined_at: string
}

interface Proposal {
  id: string
  title: string
  description: string
  creator: {
    username: string
  }
  vote_count: number
  created_at: string
}

export default function LivingWorldPage() {
  const params = useParams()
  const worldId = params.worldId as string
  const queryClient = useQueryClient()
  const [activeTab, setActiveTab] = useState('posts')

  // Fetch world details
  const { data: world, isLoading: worldLoading } = useQuery(
    ['world', worldId],
    async () => {
      const token = localStorage.getItem('authToken')
      const response = await axios.get(`/api/worlds/${worldId}/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    },
    {
      retry: false,
      onError: (error) => {
        console.error('Error fetching world:', error)
      }
    }
  )

  // Fetch world posts
  const { data: posts, isLoading: postsLoading } = useQuery(
    ['worldPosts', worldId],
    async () => {
      const token = localStorage.getItem('authToken')
      const response = await axios.get(`/api/worlds/${worldId}/posts/`, {
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

  // Fetch world members
  const { data: members, isLoading: membersLoading } = useQuery(
    ['worldMembers', worldId],
    async () => {
      const token = localStorage.getItem('authToken')
      const response = await axios.get(`/api/worlds/${worldId}/members/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data.results || response.data
    },
    {
      retry: false,
      onError: (error) => {
        console.error('Error fetching members:', error)
      }
    }
  )

  // Fetch world proposals
  const { data: proposals, isLoading: proposalsLoading } = useQuery(
    ['worldProposals', worldId],
    async () => {
      const token = localStorage.getItem('authToken')
      const response = await axios.get(`/api/worlds/${worldId}/proposals/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data.results || response.data
    },
    {
      retry: false,
      onError: (error) => {
        console.error('Error fetching proposals:', error)
      }
    }
  )

  // Create post mutation
  const createPostMutation = useMutation(
    async (content: string) => {
      const token = localStorage.getItem('authToken')
      const response = await axios.post('/api/posts/', {
        content,
        world_id: worldId
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['worldPosts', worldId])
      }
    }
  )

  // Vote mutation
  const voteMutation = useMutation(
    async ({ proposalId, choice }: { proposalId: string, choice: string }) => {
      const token = localStorage.getItem('authToken')
      const response = await axios.post('/api/votes/', {
        proposal_id: proposalId,
        choice
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['worldProposals', worldId])
      }
    }
  )

  // Get theme colors
  const getThemeColors = () => {
    if (!world?.theme_data) {
      return {
        backgroundColor: '#f8fafc',
        primaryColor: '#0ea5e9',
        secondaryColor: '#64748b'
      }
    }
    
    return {
      backgroundColor: world.theme_data.backgroundColor || '#f8fafc',
      primaryColor: world.theme_data.primaryColor || '#0ea5e9',
      secondaryColor: world.theme_data.secondaryColor || '#64748b'
    }
  }

  const themeColors = getThemeColors()

  if (worldLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!world) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">World not found</h2>
        <p className="text-gray-600">The Living World you're looking for doesn't exist.</p>
      </div>
    )
  }

  return (
    <div 
      className="min-h-screen"
      style={{ backgroundColor: themeColors.backgroundColor }}
    >
      {/* World Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 
                className="text-3xl font-bold"
                style={{ color: themeColors.primaryColor }}
              >
                {world.name}
              </h1>
              <p className="mt-2 text-gray-600 max-w-2xl">
                {world.description}
              </p>
              <div className="mt-4 flex items-center space-x-6 text-sm text-gray-500">
                <span>Created by {world.owner.username}</span>
                <span>{world.member_count} members</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            <button
              onClick={() => setActiveTab('posts')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'posts'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
              style={{
                borderColor: activeTab === 'posts' ? themeColors.primaryColor : undefined,
                color: activeTab === 'posts' ? themeColors.primaryColor : undefined
              }}
            >
              Posts
            </button>
            <button
              onClick={() => setActiveTab('members')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'members'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
              style={{
                borderColor: activeTab === 'members' ? themeColors.primaryColor : undefined,
                color: activeTab === 'members' ? themeColors.primaryColor : undefined
              }}
            >
              Members
            </button>
            <button
              onClick={() => setActiveTab('governance')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'governance'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
              style={{
                borderColor: activeTab === 'governance' ? themeColors.primaryColor : undefined,
                color: activeTab === 'governance' ? themeColors.primaryColor : undefined
              }}
            >
              Governance
            </button>
          </nav>
        </div>
      </div>

      {/* Content Area */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeTab === 'posts' && (
          <div className="space-y-6">
            {/* Create Post Form */}
            <div className="bg-white rounded-lg shadow p-6">
              <CreatePostForm
                onSubmit={createPostMutation.mutate}
                isLoading={createPostMutation.isLoading}
                themeColor={themeColors.primaryColor}
              />
            </div>

            {/* Posts Feed */}
            <div className="space-y-4">
              {postsLoading ? (
                <div className="space-y-4">
                  {[1, 2, 3].map((i) => (
                    <div key={i} className="bg-white rounded-lg shadow p-6 animate-pulse">
                      <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                      <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                    </div>
                  ))}
                </div>
              ) : posts && posts.length > 0 ? (
                posts.map((post: Post) => (
                  <div key={post.id} className="bg-white rounded-lg shadow p-6">
                    <div className="flex items-start space-x-3">
                      <div className="flex-shrink-0">
                        <div 
                          className="h-10 w-10 rounded-full flex items-center justify-center text-white font-medium"
                          style={{ backgroundColor: themeColors.primaryColor }}
                        >
                          {post.author.username.charAt(0).toUpperCase()}
                        </div>
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center space-x-2">
                          <p className="text-sm font-medium text-gray-900">
                            {post.author.username}
                          </p>
                          <span className="text-sm text-gray-500">
                            {new Date(post.created_at).toLocaleDateString()}
                          </span>
                        </div>
                        <p className="mt-1 text-gray-900">{post.content}</p>
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-12">
                  <p className="text-gray-500">No posts yet. Be the first to share something!</p>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'members' && (
          <div className="bg-white rounded-lg shadow">
            <div className="p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Members</h3>
              {membersLoading ? (
                <div className="animate-pulse space-y-3">
                  {[1, 2, 3, 4, 5].map((i) => (
                    <div key={i} className="h-12 bg-gray-200 rounded"></div>
                  ))}
                </div>
              ) : members && members.length > 0 ? (
                <ul className="divide-y divide-gray-200">
                  {members.map((member: Member) => (
                    <li key={member.id} className="py-4 flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-gray-900">{member.profile.user.username}</p>
                        <p className="text-sm text-gray-500">{member.profile.name} - {member.role}</p>
                      </div>
                      <span className="text-sm text-gray-500">{member.reputation} rep</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500">No members yet.</p>
              )}
            </div>
          </div>
        )}

        {activeTab === 'governance' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Proposals</h3>
              {proposalsLoading ? (
                <div className="animate-pulse space-y-4">
                  {[1, 2].map((i) => (
                    <div key={i} className="h-24 bg-gray-200 rounded"></div>
                  ))}
                </div>
              ) : proposals && proposals.length > 0 ? (
                <div className="space-y-4">
                  {proposals.map((proposal: Proposal) => (
                    <div key={proposal.id} className="border border-gray-200 rounded-lg p-4">
                      <h4 className="font-semibold text-gray-900">{proposal.title}</h4>
                      <p className="text-sm text-gray-600 mt-1">{proposal.description}</p>
                      <div className="flex items-center justify-between mt-4 text-xs text-gray-500">
                        <span>by {proposal.creator.username}</span>
                        <span>{proposal.vote_count} votes</span>
                      </div>
                      <div className="mt-4 flex space-x-2">
                        <button
                          onClick={() => voteMutation.mutate({ proposalId: proposal.id, choice: 'agree' })}
                          className="px-3 py-1 text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
                          disabled={voteMutation.isLoading}
                        >
                          Agree
                        </button>
                        <button
                          onClick={() => voteMutation.mutate({ proposalId: proposal.id, choice: 'disagree' })}
                          className="px-3 py-1 text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
                          disabled={voteMutation.isLoading}
                        >
                          Disagree
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500">No proposals yet.</p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
} 