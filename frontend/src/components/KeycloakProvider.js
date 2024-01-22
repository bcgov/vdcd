import React, { useState, useEffect } from 'react'
import { KeycloakContext } from '../contexts'

const KeycloakProvider = ({authClient, initOptions, LoadingComponent, children}) => {
  const [loading, setLoading] = useState(true)
  const [keycloak, setKeycloak] = useState({})

  useEffect(() => {
    authClient.init(initOptions).then(() => {
      setKeycloak(authClient)
      setLoading(false)
    })
  }, [authClient, initOptions])

  if (loading) {
    return <LoadingComponent/>
  }
  return (
    <KeycloakContext.Provider value={keycloak}>
      {children}
    </KeycloakContext.Provider>
  )
}

export default KeycloakProvider