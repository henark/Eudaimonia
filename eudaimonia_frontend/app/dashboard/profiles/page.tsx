'use client'

import { useQuery, useMutation, useQueryClient } from 'react-query'
import axios from 'axios'
import { useForm } from 'react-hook-form'

interface SmartProfile {
  id: string
  name: string
  did: string
}

type FormData = {
  name: string
}

export default function SmartProfilesPage() {
  const queryClient = useQueryClient()
  const { register, handleSubmit, reset } = useForm<FormData>()

  const { data: profiles, isLoading } = useQuery('smartProfiles', async () => {
    const token = localStorage.getItem('authToken')
    const response = await axios.get('/api/smart-profiles/', {
      headers: { Authorization: `Bearer ${token}` },
    })
    return response.data.results || response.data
  })

  const createProfileMutation = useMutation(
    async (data: FormData) => {
      const token = localStorage.getItem('authToken')
      const response = await axios.post('/api/smart-profiles/', data, {
        headers: { Authorization: `Bearer ${token}` },
      })
      return response.data
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries('smartProfiles')
        reset()
      },
    }
  )

  const onSubmit = (data: FormData) => {
    createProfileMutation.mutate(data)
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Your Smart Profiles</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Create New Profile</h2>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                Profile Name
              </label>
              <input
                id="name"
                type="text"
                {...register('name', { required: true })}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              />
            </div>
            <button
              type="submit"
              className="w-full inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              disabled={createProfileMutation.isLoading}
            >
              {createProfileMutation.isLoading ? 'Creating...' : 'Create Profile'}
            </button>
          </form>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Existing Profiles</h2>
          {isLoading ? (
            <p>Loading profiles...</p>
          ) : (
            <ul className="divide-y divide-gray-200">
              {profiles?.map((profile: SmartProfile) => (
                <li key={profile.id} className="py-4">
                  <p className="font-medium text-gray-900">{profile.name}</p>
                  <p className="text-sm text-gray-500 truncate">{profile.did || 'No DID yet'}</p>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  )
}
