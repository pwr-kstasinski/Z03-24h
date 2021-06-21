import { Component, OnInit } from '@angular/core';
import { SocketService } from '../../../services/socket.service';
import { JwtHelperService } from '@auth0/angular-jwt';
import { User, UserService } from '../../../../apiclient';
import { Router } from '@angular/router';

interface UserStatus extends User {
  online: boolean;
}


@Component({
  selector: 'app-users-status',
  templateUrl: 'users-status.component.html',
  styleUrls: ['users-status.component.scss'],
})
export class UsersStatusComponent implements OnInit {

  usersList: Array<UserStatus>;
  token: string;
  private jwtHelper: JwtHelperService = new JwtHelperService();

  constructor(private userService: UserService, private socketService: SocketService, private router: Router) {
  }

  ngOnInit(): void {
    this.token = localStorage.getItem('jwt');
    this.getUsers();
    this.listenChangeStatus();
  }

  getUsers(): void {
    const userLogin = this.getUser();
    this.userService.usersGet(this.token).subscribe(
      ({ data }: any) => this.usersList = data.filter(({ login }) => login !== userLogin) as UserStatus[],
      (err) => (console.log(err)),
      () => this.getUsersStatus());
  }

  getUsersStatus(): void {
    this.userService.onlineGet(this.token)
      .subscribe((statusArr: string[]) =>
        this.usersList.forEach((user) => user.online = statusArr.includes(user.login)));
  }

  listenChangeStatus(): void {
    this.socketService.status$.subscribe(
      ({ login, online }) => {
        if (login !== this.getUser()) {
          this.usersList.find(({ login: userLogin }) => userLogin === login).online = online;
        }
      });
  }

  getUser(): string {
    return this.jwtHelper.decodeToken(this.token).user;
  }

  openChat(id: number) {
    this.router.navigate([''], {queryParams: {user: id}});
  }

  goToGeneral() {
    this.router.navigate([''], {queryParams: {group: 0}});
  }
}
