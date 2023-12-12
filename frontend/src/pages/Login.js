import React from 'react'
import { useKeycloak } from '@react-keycloak/web'

const Login = () => {
  const { keycloak } = useKeycloak()
  const redirectUri = `${window.location.origin}/upload`
  return (
    <div>
      <button
        onClick={() => {
          keycloak.login({
            idpHint: 'idir',
            redirectUri: redirectUri
          })
        }}
      >
        Login
      </button>
    </div>
  )
}

export default Login