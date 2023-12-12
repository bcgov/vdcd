import { useEffect, useRef } from 'react'
import axios from 'axios'
import { useKeycloak } from '@react-keycloak/web'
import { API_BASE } from '../config'

const useAxios = (opts = {}) => {
  const axiosInstance = useRef()
  const { keycloak } = useKeycloak()
  
  useEffect(() => {
    const instance = axios.create({
      baseURL: API_BASE,
      ...opts,
    })
    instance.interceptors.request.use(async (config) => {
      if (keycloak.authenticated) {
        try {
          await keycloak.updateToken(30)
          config.headers = { 
            'Authorization': `Bearer ${keycloak.token}`,
          }
        } catch(error) {
          // do something here?
        }
      }
      return config
    })
    axiosInstance.current = instance

    return () => {
      axiosInstance.current = undefined
    }
  }, [opts, keycloak])

  return axiosInstance
}

export default useAxios