import { Component, ElementRef, Input, OnChanges, OnDestroy, OnInit, SimpleChanges, ViewChild } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Message, MessageService, User, UserService } from '../../../../apiclient';
import { JwtHelperService } from '@auth0/angular-jwt';
import { Router } from '@angular/router';
import { SocketService } from '../../../services/socket.service';
import { Subscription } from 'rxjs';


@Component({
  selector: 'app-chat',
  templateUrl: 'chat.component.html',
  styleUrls: ['chat.component.scss'],
})

export class ChatComponent implements OnInit, OnChanges, OnDestroy {
  messageControl = new FormControl('');
  messagesList: Array<Message> = new Array<Message>();
  token: string;
  jwtHelper = new JwtHelperService();
  userLogin: string;
  userId: number;

  usersList: {};

  subscriptions: Array<Subscription> = [];

  @Input() chatId: number;
  @Input() chatType: 'user' | 'group';
  @ViewChild('messagesRef') messagesRef: ElementRef<HTMLDivElement>;

  constructor(private messageService: MessageService, private usersService: UserService, private router: Router, private socketService: SocketService) {
    this.token = localStorage.getItem('jwt');
    this.userLogin = this.getUserLogin();
    this.userId = this.getUserId();
  }

  ngOnInit(): void {
    this.getUsers();
    this.listenToSocket();
    // this.getMessages();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.chatId || changes.chatType) {
      this.getMessages();
    }
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach((sub) => sub.unsubscribe());
  }

  getMessages(): void {
    const param: Message = {
      receiver_id: this.chatId,
      sender_id: this.userId,
      group: this.chatType === 'group',
    };

    this.messageService.messageListPost(this.token, param).subscribe(
      (data: Message[]) => {
        this.messagesList = data;
        const newMess = [];
        for (const mess of this.messagesList) {
          if (mess.unread && mess.sender_id !== this.userId) {
            newMess.push(mess.id);
            mess.unread = false;
          }
        }
        if (newMess.length > 0) {
          this.updateMessagesStatus(newMess);
          this.socketService.refresh();
        }
        this.scrollToBottom();
      },
      (err) => console.log((err)),
    );
  }

  sendMessage(): void {
    const message: Message = {
      message: this.messageControl.value,
      sender_id: this.userId,
      receiver_id: this.chatId,
      group: this.chatType === 'group',
      date: new Date().toISOString(),
    };
    this.messageService.messagePost(this.token, message).subscribe(
      (data) => {
        this.messagesList.push(message);
        this.messageControl.setValue('');
        this.scrollToBottom();
        this.socketService.refresh();
      },
      (err) => console.log(err),
    );
  }

  updateMessagesStatus(messId: number[]): void {
    this.messageService.messageStatusPut(this.token, messId).subscribe(() => {
      this.socketService.refresh();
    });
  }

  getUsers(): void {
    this.usersList = {};
    this.usersService.usersGet(this.token).subscribe((data: User[]) => {
      for (const user of data) {
        this.usersList[user.id] = user.login;
      }
    });
  }

  getUserLogin(): string {
    return this.jwtHelper.decodeToken(this.token).user;
  }

  getUserId(): number {
    return this.jwtHelper.decodeToken(this.token).id;
  }

  listenToSocket(): void {
    this.subscriptions.push(
      this.socketService.getNewMessage$().subscribe(() => this.getMessages()),
    );

    this.subscriptions.push(
      this.socketService.getReadMessageEvent$().subscribe(() => this.getMessages()),
    );

  }

  scrollToBottom(): void {
    setTimeout(() => this.messagesRef.nativeElement.scrollTop = this.messagesRef.nativeElement.scrollHeight
      , 30);
  }
}
