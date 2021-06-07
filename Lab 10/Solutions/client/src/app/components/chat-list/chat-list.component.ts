import { Component, OnInit } from '@angular/core';
import { SocketService } from '../../../services/socket.service';
import { JwtHelperService } from '@auth0/angular-jwt';
import { Router } from '@angular/router';
import { Chat, ChatService, Message, User, UserService } from '../../../../apiclient';

interface UserStatus extends User {
  online: boolean;
}


@Component({
  selector: 'app-users-status',
  templateUrl: 'chat-list.component.html',
  styleUrls: ['chat-list.component.scss'],
})
export class ChatListComponent implements OnInit {

  usersList: Map<number, User>;
  token: string;
  chatList: Chat[];
  private jwtHelper: JwtHelperService = new JwtHelperService();

  constructor(
    private userService: UserService,
    private chatListService: ChatService,
    private socketService: SocketService,
    private router: Router) {
  }

  ngOnInit(): void {
    this.token = localStorage.getItem('jwt');
    this.getUsers();
    this.listenSocket();
  }

  getUsers(): void {
    this.userService.usersGet(this.token).subscribe(
      (data: User[]) => {
        this.usersList = new Map(data.map((user: User) => [user.id, user]));
      },
      (err) => (console.log(err)),
      () => this.getChatList());
  }

  getChatList(): void {
    this.chatListService.chatListGet(this.token).subscribe((chatList) => {
      this.chatList = chatList;
      this.userService.onlineGet(this.token)
        .subscribe((statusArr: number[]) => {
            this.chatList.forEach((chat: Chat) => {
              if (!chat.group) {
                chat.status = statusArr.includes(chat.id);
              }
            });
            this.chatList.sort((a, b) => {
              if (a.message?.date && b.message?.date) {
                return new Date(b.message.date).getTime() - new Date(a.message.date).getTime();
              } else if (a.message?.date) {
                return -1;
              } else if (b.message?.date) {
                return 1;
              } else if (a.status && !b.status) {
                return -1;
              } else if (!a.status && b.status) {
                return 1;
              } else {
                return a.name.localeCompare(b.name);
              }
            });
          },
        )
      ;
    });
  }

  listenSocket(): void {
    this.socketService.getStatusChange$().subscribe(
      ({ user_id, online }) => {
        if (user_id !== this.getUserId()) {
          this.chatList.find(({ id, group }) => !group && user_id === id).status = online;
        }
        this.getChatList();
      });

    this.socketService.getNewMessage$().subscribe(() => this.getChatList());
    this.socketService.getRegisterNewChat$().subscribe(() => this.getChatList());
    this.socketService.getRefresh$().subscribe(() => this.getChatList());
  }

  getUser(): string {
    return this.jwtHelper.decodeToken(this.token).user;
  }

  getUserId(): number {
    return this.jwtHelper.decodeToken(this.token).id;
  }

  openChat(chat: Chat): void {
    const queryParams = chat.group ? { group: chat.id } : { user: chat.id };
    this.router.navigate([''], { queryParams });
  }

  getStatusClass(chat: Chat): string {
    if (chat.status == null) {
      return '';
    } else if (chat.status) {
      return 'chat-list__status--online';
    } else {
      return 'chat-list__status--offline';
    }
  }

  getMessagePrefix(message: Message): string {
    if (message == null) {
      return '';
    } else if (message.sender_id === this.getUserId()) {
      return 'Ty: ';
    } else if (message.group) {
      const login = this.usersList.get(message.sender_id).login;
      return `${login}: `;
    } else {
      return '';
    }

  }

  getDateFormat(date: string): string {
    if (date == null || date === '') return '';
    const yest = new Date();
    yest.setDate(yest.getDate() - 1);
    return new Date(date) < yest ? 'dd.MM HH:mm' : 'HH:mm';
  }

  getFirstLetter(str: string): string {
    return str[0].toUpperCase();
  }
}
