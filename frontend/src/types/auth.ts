export interface UserCredentials {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface ErrorDetail {
  loc: string[];
  msg: string;
  type: string;
}

export interface ApiError {
  detail: string | ErrorDetail[];
}

export interface User {
  id: number;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  is_verified: boolean;
}
