import { Component, OnInit } from '@angular/core';
import { SocketService } from '../../../services/socket.service';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { BehaviorSubject } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: 'home.component.html',
  styleUrls: ['home.component.scss'],
  providers: [SocketService],
})

export class HomeComponent implements OnInit {

  chatType$: BehaviorSubject<'user' | 'group'> = new BehaviorSubject<'user' | 'group'>('group');
  chatId$: BehaviorSubject<number> = new BehaviorSubject<number>(0);


  constructor(private socketService: SocketService, private router: Router, private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      if (params.user) {
        this.chatType$.next( 'user');
        this.chatId$.next(params.user);
      } else if (params.group) {
        this.chatType$.next('group');
        this.chatId$.next(params.group);
      }
    });
  }


  logout(): void {
    localStorage.removeItem('jwt');
    this.socketService.disconnect();
    this.router.navigate(['login']);
  }
}
