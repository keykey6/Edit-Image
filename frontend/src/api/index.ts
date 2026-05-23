import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

export interface ProcessParams {
  module: string
  file: File
  params?: Record<string, unknown>
}

export async function processImage({ module, file, params }: ProcessParams) {
  const formData = new FormData()
  formData.append('file', file)
  if (params) {
    formData.append('params', JSON.stringify(params))
  }
  const res = await api.post(`/${module}/process`, formData, {
    responseType: 'blob',
  })
  return URL.createObjectURL(res.data)
}

export async function processImageJson({ module, file, params }: ProcessParams) {
  const formData = new FormData()
  formData.append('file', file)
  if (params) {
    formData.append('params', JSON.stringify(params))
  }
  const res = await api.post(`/${module}/process`, formData)
  return res.data
}

export async function processImagesZip({ module, files, params }: {
  module: string
  files: File[]
  params?: Record<string, unknown>
}) {
  const formData = new FormData()
  for (const f of files) {
    formData.append('files', f)
  }
  if (params) {
    formData.append('params', JSON.stringify(params))
  }
  const res = await api.post(`/${module}/process`, formData, {
    responseType: 'blob',
  })
  return res.data
}

export default api
