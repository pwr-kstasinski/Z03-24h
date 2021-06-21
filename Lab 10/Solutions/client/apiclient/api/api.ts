export * from './auth.service';
import { AuthService } from './auth.service';
export * from './auth.serviceInterface'
export * from './chat.service';
import { ChatService } from './chat.service';
export * from './chat.serviceInterface'
export * from './group.service';
import { GroupService } from './group.service';
export * from './group.serviceInterface'
export * from './message.service';
import { MessageService } from './message.service';
export * from './message.serviceInterface'
export * from './user.service';
import { UserService } from './user.service';
export * from './user.serviceInterface'
export const APIS = [AuthService, ChatService, GroupService, MessageService, UserService];
