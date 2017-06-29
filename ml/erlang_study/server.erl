
-module(server).
-export([start/0]).

-include("common.hrl").


start() ->
    {ok, ListenSocket} = gen_tcp:listen(?SERVER_PORT, [binary, {packet, 0}, {active, false}]),
    spawn(fun() -> proc_accept(ListenSocket) end),
    register(regname_worker, spawn(fun() -> proc_start_worker() end)).


% 每一个TCP连接一个worker,他们的消息都发往这儿
worker() ->
    receive
        {protocol, Body, Len} ->
            proc_protocol(Body, Len);
        {session_id, Pid} ->
            put(session_id, Pid);
        _ ->
            io:format("unkonwn mesage~n")
    end,
    worker().



proc_start_worker() ->
    receive
        {start_new_worker, Pid} ->
            WorkerPid = spawn(fun() -> worker() end),
            WorkerPid ! { session_id, Pid },
            Pid ! {start_new_worker_ok, WorkerPid},
            io:format("new job worker start ok~n");
        _ ->
        do_nothing
    end,
    proc_start_worker().


proc_accept(ListenSocket) ->
    case gen_tcp:accept(ListenSocket) of 
        {ok, Client} ->
            % io:format("[S] Accept OK!~n"),
            spawn(fun() -> proc_accept(ListenSocket) end),
            regname_worker ! {start_new_worker, self()},
            receive
                {start_new_worker_ok, Pid} ->
                    put(proxy_pid, Pid),
                    proc_work(Client, <<>>)
            end;
        {error, Reason} ->
            io:format("[S] Accept Failed: ~p~n", [Reason])
    end.



proc_work(Client, Bin) -> 
    case gen_tcp:recv(Client, 0) of
        {ok, Data} ->
            % io:format("[S] Recv:~p~n", [Data]),
            BinLeft = proc_data(<<Bin/binary, Data/binary>>),
            proc_work(Client, BinLeft);
        {error, Reason} ->
            io:format("[S] Closed:~p~n", [Reason])
    end.



proc_data(Bin) when byte_size(Bin) == 0 ->
    <<>>;
proc_data(Bin) when byte_size(Bin) < 10 ->
    Bin;
proc_data(Bin) ->
    % io:format("~p~n", [Bin]),
    Head = ?PACKET_HEAD,
    case Bin of
        <<Head:4/binary, Len:16, Body/binary>> ->
            if
                Len < 4 ->
                    erlang:error("Invalid Packet Len~n");
                true ->
                    Pid = get(proxy_pid),
                    Pid ! {protocol, Body, Len-4},
                    <<>>
            end;
        _ ->
            io:format("checkout...~n"),
            <<_Drop:8, BinLeft/binary>> = Bin,
            BinLeft
    end.



proc_protocol(<<ProtoId:32, Data/binary>> = _Bin, _DataLen) ->
    % io:format("ProtoId=~p, Data=~p, Len=~p~n", [ProtoId, Data, _DataLen]),
    
    case ProtoId of
        1 ->
            io:format("Content: Hello...~n");
        2 ->
            io:format("Content: How are you!~n");
        _Pid ->
            io:format("Unknown ProtoId:~p, Data=~p~n", [_Pid, Data])
    end.
