export * from './auth.service';
import { AuthService } from './auth.service';
export * from './auth.serviceInterface'
export * from './message.service';
import { MessageService } from './message.service';
export * from './message.serviceInterface'
export const APIS = [AuthService, MessageService];
