///////////////////////////////
////////////// System messages
///////////////////////////////

---types---

msgs_ack#62d6b459 msg_ids:Vector<long> = MsgsAck;

bad_msg_notification#a7eff811 bad_msg_id:long bad_msg_seqno:int error_code:int = BadMsgNotification;
bad_server_salt#edab447b bad_msg_id:long bad_msg_seqno:int error_code:int new_server_salt:long = BadMsgNotification;

msgs_state_req#da69fb52 msg_ids:Vector<long> = MsgsStateReq;
msgs_state_info#04deb57d req_msg_id:long info:string = MsgsStateInfo;
msgs_all_info#8cc0d131 msg_ids:Vector<long> info:string = MsgsAllInfo;

msg_detailed_info#276d3ec6 msg_id:long answer_msg_id:long bytes:int status:int = MsgDetailedInfo;
msg_new_detailed_info#809db6df answer_msg_id:long bytes:int status:int = MsgDetailedInfo;

msg_resend_req#7d861a08 msg_ids:Vector<long> = MsgResendReq;
msg_resend_ans_req#8610baeb msg_ids:Vector<long> = MsgResendReq;

rpc_result#f35c6d01 req_msg_id:long result:Object = RpcResult;
rpc_error#2144ca19 error_code:int error_message:string = RpcError;

rpc_answer_unknown#5e2ad36e = RpcDropAnswer;
rpc_answer_dropped_running#cd78e586 = RpcDropAnswer;
rpc_answer_dropped#a43ad8b7 msg_id:long seq_no:int bytes:int = RpcDropAnswer;

// future_salt#0949d9dc valid_since:int valid_until:int salt:long = FutureSalt;  // Parsed manually
// future_salts#ae500895 req_msg_id:long now:int salts:vector<future_salt> = FutureSalts;  // Parsed manually

pong#347773c5 msg_id:long ping_id:long = Pong;

destroy_session_ok#e22045fc session_id:long = DestroySessionRes;
destroy_session_none#62d350c9 session_id:long = DestroySessionRes;

new_session_created#9ec20908 first_msg_id:long unique_id:long server_salt:long = NewSession;

//// 0x5bb8e511 = hex(crc32(b"message msg_id:long seqno:int bytes:int body:Object = Message"))
// message#5bb8e511 msg_id:long seqno:int bytes:int body:Object = Message;  // Parsed manually
// msg_container#73f1f8dc messages:vector<message> = MessageContainer;  // Parsed manually
// msg_copy#e06046b2 orig_message:Message = MessageCopy;  // Not used
// gzip_packed#3072cfa1 packed_data:string = Object;  // Parsed manually

http_wait#9299359f max_delay:int wait_after:int max_wait:int = HttpWait;

//// 0xd433ad73 = hex(crc32(b"ipPort ipv4:int port:int = IpPort"))
// ipPort ipv4:int port:int = IpPort;
// help.configSimple#d997c3c5 date:int expires:int dc_id:int ip_port_list:Vector<IpPort> = help.ConfigSimple;

ipPort#d433ad73 ipv4:int port:int = IpPort;
ipPortSecret#37982646 ipv4:int port:int secret:bytes = IpPort;
accessPointRule#4679b65f phone_prefix_rules:string dc_id:int ips:vector<IpPort> = AccessPointRule;
help.configSimple#5a592a6c date:int expires:int rules:vector<AccessPointRule> = help.ConfigSimple;

// tlsClientHello blocks:vector<TlsBlock> = TlsClientHello;
//
// tlsBlockString data:string = TlsBlock;
// tlsBlockRandom length:int = TlsBlock;
// tlsBlockZero length:int = TlsBlock;
// tlsBlockDomain = TlsBlock;
// tlsBlockGrease seed:int = TlsBlock;
// tlsBlockScope entries:Vector<TlsBlock> = TlsBlock;

---functions---

rpc_drop_answer#58e4a740 req_msg_id:long = RpcDropAnswer;

get_future_salts#b921bd04 num:int = FutureSalts;

ping#7abe77ec ping_id:long = Pong;
ping_delay_disconnect#f3427b8c ping_id:long disconnect_delay:int = Pong;

destroy_session#e7512126 session_id:long = DestroySessionRes;

contest.saveDeveloperInfo#9a5f6e95 vk_id:int name:string phone_number:string age:int city:string = Bool;
