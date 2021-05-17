import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { ApiModule, Configuration } from '../../apiclient';
import { AuthGuard } from '../tools/auth.guard';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { SocketIoConfig, SocketIoModule } from 'ngx-socket-io';
import { RegisterComponent } from './pages/register/register.component';
import { LoginComponent } from './pages/login/login.component';
import { ChatComponent } from './components/chat/chat.component';
import { HomeComponent } from './pages/home/home.component';
import { UsersStatusComponent } from './components/users-status/users-status.component';

const url = 'http://127.0.0.1:5000';
const socketConfig: SocketIoConfig = { url, options: {} };
const apiConfig: Configuration = new Configuration({ basePath: url });

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    ChatComponent,
    HomeComponent,
    UsersStatusComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    HttpClientModule,
    ApiModule.forRoot(() => apiConfig),
    ReactiveFormsModule,
    SocketIoModule.forRoot(socketConfig),
  ],
  providers: [AuthGuard],
  bootstrap: [AppComponent],
})
export class AppModule {
}
