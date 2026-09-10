const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })

  if (!response.ok) {
    throw new Error('No fue posible comunicarse con la API')
  }

  if (response.status === 204) {
    return null
  }

  return response.json()
}

export function getProjects() {
  return request('/projects')
}

export function createProject(payload) {
  return request('/projects', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function updateProject(projectId, payload) {
  return request(`/projects/${projectId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export function deleteProject(projectId) {
  return request(`/projects/${projectId}`, {
    method: 'DELETE',
  })
}

export function createActivity(projectId, payload) {
  return request(`/projects/${projectId}/activities`, {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function updateActivity(projectId, activityId, payload) {
  return request(`/projects/${projectId}/activities/${activityId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export function deleteActivity(projectId, activityId) {
  return request(`/projects/${projectId}/activities/${activityId}`, {
    method: 'DELETE',
  })
}