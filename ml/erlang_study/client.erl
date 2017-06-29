
-module(client).
-export([connect/0, connect/1, client_timerout/1]).

-include("common.hrl").




connect() ->
    connect(10).



connect(0) ->
    ok;
connect(N) ->
    spawn(?MODULE, connect, [N-1]),
    case gen_tcp:connect(?SERVER_ADDR, ?SERVER_PORT, [binary, {packet, 0}, {active, false}]) of
    {ok, Server} ->
        io:format("[C] Connect 2 Server OK!~n"),
        % timer:apply_after(3000, ?MODULE, client_timerout, [Server]),
        proc_client(Server);
    {error, Reason} ->
        io:format("[C] Connect 2 Server Failed: ~p~n", [Reason])
    end.
    




proc_client(Server) ->
    case gen_tcp:recv(Server, 0, 3000) of
    {ok, Data} ->
        io:format("[C] recv data: ~p~n", [Data]),
        proc_client(Server);
    {error, timeout} ->
        io:format("[C] recv timeout ...~n"),
        client_timerout(Server),
        proc_client(Server);
    {error, Reason} ->
        io:format("[C] recv error: ~p~n", [Reason]),
        gen_tcp:close(Server)
    end.



client_timerout(Server) ->
    % random:seed(erlang:now()),
    Pid = random:uniform(5),
    Data = get_data(<<>>, random:uniform(20)),
    case send_server(Server, Pid, Data) of
        true ->
            true;%timer:apply_after(3000, ?MODULE, client_timerout, [Server]);
        false ->
            io:format("closed...~n")
    end.



send_server(Peer, ProtoId, Data)->
    Head = ?PACKET_HEAD,
    Len = byte_size(Data) + 4,
    Packet = <<Head/binary, Len:16, ProtoId:32, Data/binary>>,
    % io:format("ProtoId=~p, Data=~p, Len=~p.~n", [ProtoId, Data, Len-4]),
    case gen_tcp:send(Peer, Packet) of
        {error, Reason} ->
            io:format("Closed, ~p~n", [Reason]),
            false;
        ok ->
            true
    end.



get_data(Data, 0) ->
    Data;
get_data(Data, Size) ->
    Ch = random:uniform(256),
    Data2 = <<Ch:8, Data/binary>>,
    get_data(Data2, Size-1).
