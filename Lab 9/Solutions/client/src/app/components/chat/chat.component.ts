import { Component, ElementRef, Input, OnChanges, OnInit, SimpleChanges, ViewChild } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Message, MessageService, User, UserService } from '../../../../apiclient';
import { JwtHelperService } from '@auth0/angular-jwt';
import { Router } from '@angular/router';


@Component({
  selector: 'app-chat',
  templateUrl: 'chat.component.html',
  styleUrls: ['chat.component.scss'],
})

export class ChatComponent implements OnInit, OnChanges {
  messageControl = new FormControl('');
  messagesList: Array<Message> = new Array<Message>();
  token: string;
  jwtHelper = new JwtHelperService();
  userLogin: string;
  userId: number;

  usersList: {};

  @Input() chatId: number;
  @Input() chatType: 'user' | 'group';
  @ViewChild('messagesRef') messagesRef: ElementRef<HTMLDivElement>;

  constructor(private messageService: MessageService, private usersService: UserService, private router: Router) {
  }

  ngOnInit(): void {
    this.token = localStorage.getItem('jwt');
    this.userLogin = this.getUserLogin();
    this.userId = this.getUserId();
    this.getUsers();
    this.getMessages();
  }
  ngOnChanges(changes: SimpleChanges): void {
    if(changes.chatId && changes.chatType) {
      this.getMessages();
    }
  }

  getMessages(): void {
    const param: Message = {
      receiverId: this.chatId,
      senderId: this.getUserId(),
      group: this.chatType === 'group',
    };
    this.messageService.messageListPost(this.token, param).subscribe(
      ({ data }: any) => {
        this.messagesList = data;
        this.scrollToBottom();
      },
      (err) => console.log((err)),
    );
  }

  sendMessage(): void {
    const message: Message = {
      message: this.messageControl.value,
      senderId: this.getUserId(),
      receiverId: this.chatId,
      group: this.chatType === 'group',
    };
    this.messageService.messagePost(this.token, message).subscribe(
      (data) => {
        this.messagesList.push(message);
        this.messageControl.setValue('');
        this.scrollToBottom();
      },
      (err) => console.log(err),
    );
  }

  getUsers(): void {
    this.usersList = {};
    this.usersService.usersGet(this.token).subscribe(({ data }: any) => {
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


  scrollToBottom(): void {
    console.log(this.messagesRef.nativeElement.scrollTop);
    setTimeout(() => this.messagesRef.nativeElement.scrollTop = this.messagesRef.nativeElement.scrollHeight
      , 30);
    console.log(this.messagesRef.nativeElement.scrollTop);
  }
}
