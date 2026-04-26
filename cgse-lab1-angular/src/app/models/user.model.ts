export interface User {
  id: string;
  email: string;
  name: string;
  password?: string;
  role?: string;
  isAdmin?: boolean;
  createdAt?: Date;
  updatedAt?: Date;
}

export interface UserCreateRequest {
  email: string;
  password: string;
  name: string;
}

export interface UserUpdateRequest {
  name?: string;
  email?: string;
}
