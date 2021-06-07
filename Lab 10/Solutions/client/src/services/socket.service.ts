import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { BehaviorSubject, config, Observable } from 'rxjs';
import { Router } from '@angular/router';

@Injectable()
export class CustomSocket extends Socket {

  constructor() {
    super({
      url: 'http://127.0.0.1:5000', options: {
        query: {
          token: localStorage.getItem('jwt'),
        },
      },
    });
  }
}

@Injectable()
export class SocketService {

  private status$ = this.socket.fromEvent('status');
  private readMessage$ = this.socket.fromEvent('read_message');
  private registerNewChat$ = this.socket.fromEvent('register_new_chat');
  private newMessage$ = this.socket.fromEvent('new_message');
  private refresh$  = new BehaviorSubject(0);

  constructor(private socket: CustomSocket, private router: Router) {
    this.connect();
  }

  async connect(): Promise<void> {
    const res = await this.socket.connect();
    // if (res.disconnected) {
    //   this.router.navigate(['login']);
    // }
  }

  getStatusChange$(): Observable<any> {
    return this.status$;
  }

  getReadMessageEvent$(): Observable<any> {
    return this.readMessage$;
  }

  getRegisterNewChat$(): Observable<any> {
    return this.registerNewChat$;
  }

  getNewMessage$(): Observable<any> {
    return this.newMessage$;
  }

  disconnect(): void {
    this.socket.disconnect();
  }

  refresh(): void {
    console.log('refff');
    this.refresh$.next(0);
  }

  getRefresh$(): Observable<any> {
    return this.refresh$;
  }


}
