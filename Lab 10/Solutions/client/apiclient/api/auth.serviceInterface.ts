/**
 * Messenger API
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */
import { HttpHeaders }                                       from '@angular/common/http';

import { Observable }                                        from 'rxjs';

import { Auth } from '../model/models';
import { Token } from '../model/models';


import { Configuration }                                     from '../configuration';



export interface AuthServiceInterface {
    defaultHeaders: HttpHeaders;
    configuration: Configuration;

    /**
     * Login user
     * 
     * @param auth 
     */
    loginPost(auth: Auth, extraHttpRequestParams?: any): Observable<Token>;

    /**
     * Register user
     * 
     * @param auth 
     */
    registerPost(auth: Auth, extraHttpRequestParams?: any): Observable<{}>;

}
