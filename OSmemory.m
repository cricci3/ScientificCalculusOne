classdef OSmemory
    methods(Static)
        function [memory_used] = memory()
            if ispc() 
                % Se il sistema operativo è Windows
                m = memory();
                memory_used = m.MemUsedMATLAB;
            else
                % Se il sistema operativo è Linux
                [~, result] = system('free -b | grep Mem');
                memory_info = strsplit(result);
                memory_used = str2double(memory_info{3});
            end
        end
    end
end