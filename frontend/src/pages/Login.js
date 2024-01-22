import React from 'react'
import useKeycloak from '../hooks/useKeycloak'

const Login = () => {
  const keycloak = useKeycloak()
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