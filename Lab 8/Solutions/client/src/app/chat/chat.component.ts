import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MessageDTO, MessageService } from '../../../apiclient';
import { JwtHelperService } from '@auth0/angular-jwt';
import { Router } from '@angular/router';


@Component({
  selector: 'app-chat',
  templateUrl: 'chat.component.html',
  styleUrls: ['chat.component.scss'],
})

export class ChatComponent implements OnInit {
  messageControl = new FormControl('');
  messagesList: Array<MessageDTO> = new Array<MessageDTO>();
  token: string;
  jwtHelper = new JwtHelperService();
  user: string;

  @ViewChild('messagesRef') messagesRef: ElementRef<HTMLDivElement>;

  constructor(private messageService: MessageService, private router: Router) {
  }

  ngOnInit(): void {
    this.token = localStorage.getItem('jwt');
    this.user = this.getUser();
    this.getMessages();
  }

  getMessages(): void {
    this.messageService.messageGet(this.token).subscribe(
      (data: MessageDTO[]) => {
        this.messagesList = data;
        this.scrollToBottom();
      },
      (err) => console.log((err)),
    );
  }

  sendMessage(): void {
    const message: MessageDTO = {
      message: this.messageControl.value,
      sender: this.user,
      receiver: 'general',
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

  getUser(): string {
    return this.jwtHelper.decodeToken(this.token).user;
  }

  scrollToBottom(): void {
    console.log(this.messagesRef.nativeElement.scrollTop);
    setTimeout(() => this.messagesRef.nativeElement.scrollTop = this.messagesRef.nativeElement.scrollHeight
      , 30);
    console.log(this.messagesRef.nativeElement.scrollTop);
  }

  logout(): void {
    localStorage.removeItem('jwt');
    this.router.navigate(['login']);
  }
}
