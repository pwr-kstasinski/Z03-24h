import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { Observable } from 'rxjs';

@Injectable()
export class SocketService {

  status$ = this.socket.fromEvent('status');

  constructor(private socket: Socket) {
    this.socket.connect();
    this.socket.emit('auth', localStorage.getItem('jwt'));
  }

  getStatusChange$(): Observable<any> {
    return this.status$;
  }

  disconnect(): void {
    this.socket.disconnect();
  }


}
