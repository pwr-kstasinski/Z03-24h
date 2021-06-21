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


export interface Message { 
    date?: string;
    /**
     * is group message
     */
    group?: boolean;
    id?: number;
    /**
     * message from sender to receiver
     */
    message?: string;
    /**
     * message receiver id or group id
     */
    receiver_id?: number;
    /**
     * message sender id
     */
    sender_id?: number;
    unread?: boolean;
}

