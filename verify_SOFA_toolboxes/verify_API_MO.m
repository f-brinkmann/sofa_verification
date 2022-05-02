close all; clear; clc

% count errors and files
num_errors = 0;
num_warnings = 0;
num_files = 0;
num_missing = 0;

% directories containing test data
basedir = 'C:\Users\panik\Documents\Code\Python\pyfar\sofar_verification_rules\data';
data_dirs = {'deprecations'
             'general_dependencies'
             'restricted_dimensions'
             'restricted_values'
             'specific_dependencies'};

delete verify_API_MO.txt
diary verify_API_MO.txt
diary on

% loop directories
for dd = 1:length(data_dirs)
    files = dir(fullfile(basedir, data_dirs{dd}, '*.sofa'));
    
    % loop files
    for ff = 1:length(files)
        % current file
        file = fullfile(files(ff).folder, files(ff).name);
        
        if strfind(file, '=missing.sofa')
            num_missing = num_missing + 1;
        end
        
        % load file and check if errors during reading appear (they should)
        try
            warning('');  % clear last warning
            H = SOFAload(file);
            num_files = num_files + 1;
            
            % check for warnings
            [warnMsg, warnId] = lastwarn;
            if ~isempty(warnMsg)
                num_warnings = num_warnings + 1;
                disp(fullfile(data_dirs{dd}, files(ff).name))
                disp(' ')
            end
        catch ME
            num_files = num_files + 1;
            num_errors = num_errors + 1;
            disp(fullfile(data_dirs{dd}, files(ff).name))
            disp(ME.message)
            disp(' ')
        end
            
    end
end

disp('-----------------------------------------')
disp('SUMMARY')
disp([num2str(num_files) ' files'])
disp([num2str(num_errors) ' errors'])
disp([num2str(num_warnings) ' warnings'])

diary off