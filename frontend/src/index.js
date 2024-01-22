import React from 'react'
import ReactDOM from 'react-dom/client'
import Keycloak from 'keycloak-js'
import KeycloakProvider from './components/KeycloakProvider'
import {
  KEYCLOAK_CLIENT_ID,
  KEYCLOAK_REALM,
  KEYCLOAK_URL
} from './config'
import Loading from './components/Loading'
import AppRouter from './router'

const keycloak = new Keycloak({
  clientId: KEYCLOAK_CLIENT_ID,
  realm: KEYCLOAK_REALM,
  url: KEYCLOAK_URL
})

const keycloakInitOptions = {
  onLoad: 'check-sso',
  pkceMethod: 'S256'
}

const root = ReactDOM.createRoot(document.getElementById('root'))
root.render(
  <KeycloakProvider
    authClient={keycloak}
    initOptions={keycloakInitOptions}
    LoadingComponent={Loading}
  >
    <AppRouter/>
  </KeycloakProvider>
)
