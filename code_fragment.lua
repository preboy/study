



-- ZeroTable
-------------------------------------------

-- Ϊ������һЩĬ��ֵ
DefaultValue = function(t, val)
    assert(val, "val must be present.")
    local _mtable =
    {
        __index = function(t, n)
            rawset(t, n, val)
            return val
        end,
    }
    setmetatable(t, _mtable)
end


-- ����δ��ֵ��������Ϊ0
ZeroTable = function(t)
    DefaultValue(t, 0)
end

local ttt = {}
DefaultValue(ttt, {"i come", "i fuck", "i phone", })

zcg_print(ttt.str)
zcg_print(ttt[223])



-- ���㱦��100���mysql����
select DATE_ADD('2014-04-07',interval 100 day)
