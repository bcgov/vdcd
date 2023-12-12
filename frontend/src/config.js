export const KEYCLOAK_CLIENT_ID = window.vdcd_config
  ? window.vdcd_config.REACT_APP_KEYCLOAK_CLIENT_ID
  : process.env.REACT_APP_KEYCLOAK_CLIENT_ID

export const KEYCLOAK_REALM = window.vdcd_config
  ? window.vdcd_config.REACT_APP_KEYCLOAK_REALM
  : process.env.REACT_APP_KEYCLOAK_REALM

export const KEYCLOAK_URL = window.vdcd_config
  ? window.vdcd_config.REACT_APP_KEYCLOAK_URL
  : process.env.REACT_APP_KEYCLOAK_URL

export const API_BASE = window.vdcd_config
  ? window.vdcd_config.REACT_APP_API_BASE
  : process.env.REACT_APP_API_BASE