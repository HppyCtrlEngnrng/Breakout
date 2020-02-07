using Sockets;

function Angle180(a::Float32)
    if (a < 180)
        return a;
    else
        return a - 360;
    end
end

function main(localport, remoteport)
    udp = UDPSocket();
    bind(udp, ip"127.0.0.1", localport);
    snd = 0.0f0;
    K_dist = -20.0f0;
    K_angle = 10.0f0;
    K_ang_vel = 1.0f0;
    flags = 0;
    ang_prev = 0.0f0;
    dt = 1/20.0f0;

    while (true)
        rcvd = recv(udp);
        
        if ( length(rcvd) >= 13 )
            pos_ref = reinterpret(Float32, rcvd[1:4])[1];
            base_pos = reinterpret(Float32, rcvd[5:8])[1];
            pole_angle = Angle180(reinterpret(Float32, rcvd[9:12])[1]);
            flags = rcvd[13];
        end

        if (flags & 0x20 != 0) break; end
        if (flags & 0x80 != 0) ang_prev = 0.0f0; end

        ang_vel = (pole_angle - ang_prev) / dt;
        snd = K_dist*(pos_ref - base_pos) - K_angle*pole_angle - K_ang_vel * ang_vel;

        send(udp, ip"127.0.0.1", remoteport, reinterpret(UInt8, [snd]));

        ang_prev = pole_angle;
    end
end