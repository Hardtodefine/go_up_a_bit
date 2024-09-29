var fs = require("fs-extra");
const path = require('path');
const { nameReg, miniprogram, list, status, listout, newbasecode } = {
    nameReg: /^[\u4e00-\u9fa50-4Z]+$/,
    miniprogram: "miniprogram",
    status: ["{waiting}", "{working}", "{prepared}"],
    list: './doc/list.csv',
    listout: './doc/listout.csv',
    newbasecode: 'basecode',
}
const { pinyin } = require('pinyin-pro');
const fn = {
    getMiniProgramName(e) {
        return e.find(item => nameReg.test(item));
    },
    getFullSpellName(e) {
        const value = this.getMiniProgramName(e);
        return pinyin(value, { v: true, toneType: 'none', type: 'array' }).join('');
    },
    getFirstSpellName(e) {
        const value = this.getMiniProgramName(e);
        return pinyin(value, { v: true, pattern: 'first', toneType: 'none', type: 'array' }).join('').toUpperCase();
    },
    getAppid(e) {
        return e.find(item => item.length === 18 && item.startsWith('wx'));
    },
    csv_to_array(str, delimiter = ",", outputType = "values", includeHeader = false) {
        const header_cols = str.slice(0, str.indexOf("\n")).split(delimiter);
        const row_data = str.slice(str.indexOf("\n") + 1).split("\n");
        const arr = row_data.map(row => {
            const values = row.split(delimiter);
            if (outputType === "el") {
                return header_cols.reduce((object, header, index) => {
                    object[header] = values[index];
                    return object;
                }, {});
            }
            return values;
        });
        if (includeHeader) arr.unshift(header_cols);
        return arr;
    },
};
const cliProgress = require("cli-progress")
const pb1 = new cliProgress.SingleBar({}, cliProgress.Presets.legacy)

// 主流程开始
let originArray = loadArray();
function loadArray() {
    let configPath = path.resolve(list);
    let fileContent = fs.readFileSync(configPath, 'UTF8');
    return fn.csv_to_array(fileContent);
}
const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
})
function confirmInput(promptMessage, defaultValue, useJudge = true) {
    return new Promise((resolve) => {
        readline.question(promptMessage, (input) => {
            resolve(useJudge ? judge(input, defaultValue) : input);
        });
    });
}
function judge(e, def) {
    if (e.toLowerCase() == 'y' || e.toLowerCase() == 'yes') {
        return true
    } else if (e.toLowerCase() == 'no' || e.toLowerCase() == 'n' || e.toLowerCase() == 'not') {
        return false
    } else if (e.trim() == '') {
        return def
    }
}
async function mainFlow() {
    const shouldOutputFolders = await confirmInput('按列表index范围输出小程序文件夹? Y/n  ', true);
    
    if (shouldOutputFolders) {
        const rangeInput = await confirmInput('输出范围? 例如输入1,3输出1,2,3行 或者输入数字输出单行', '',false);
        let selectedList = [];
        const dividerIndex = rangeInput.search(/[,.-\/_]/);
        
        if (dividerIndex === -1) {
            const lineNumber = parseInt(rangeInput) - 1;
            if (lineNumber < originArray.length) {
                selectedList.push(originArray[lineNumber]);
            }
        } else {
            const start = parseInt(rangeInput.slice(0, dividerIndex)) - 1;
            const end = parseInt(rangeInput.slice(dividerIndex + 1)) - 1;
            selectedList = originArray.slice(start, end + 1);
        }
        
        console.log('要输出的小程序为', selectedList.map(item => fn.getMiniProgramName(item)));
        await clearAndProcess(selectedList);
    } else {
        const statusInput = await confirmInput('按状态输出小程序文件夹? 输入状态例如 working  ', '',false);
        const selectedStatus = status.find(item => item.includes(statusInput));
        if (selectedStatus) {
            const filteredArray = filterArrayByStatus(originArray, selectedStatus);
            
            await clearAndProcess(filteredArray);
        } else {
            readline.close();
        }
    }
}
function filterArrayByStatus(arr, status) {
    const regex = new RegExp(status + '\\s*');// 创建一个正则表达式，匹配 '{working}' 和 '{working}\r'
    return arr.filter(item => item.some(field => regex.test(field)));// 检查数组中的任意项
}
async function clearAndProcess(targetList) {
    const shouldClear = await confirmInput('先清空目标列表? y/N  ', false);
    
    if (shouldClear) {
        fs.emptyDirSync(path.resolve(miniprogram));
    }
    
    processTargets(targetList);
    readline.close();
}
function outputLog(dataArray) {
    // 将数组转换为 CSV 格式字符串
    const csvString = dataArray.map(row => row.join(',')).join('\n');

    // 检查文件是否存在，如果不存在则创建文件
    fs.access(listout, fs.constants.F_OK, (err) => {
        if (err) {
            // 文件不存在，创建文件
            fs.writeFile(listout, csvString + '\n', 'utf8', (writeErr) => {
                if (writeErr) {
                    console.error('创建文件时发生错误:', writeErr);
                } else {
                    console.log('文件已成功创建并写入数据');
                }
            });
        } else {
            // 文件存在，追加数据
            fs.appendFile(listout, csvString + '\n', 'utf8', (appendErr) => {
                if (appendErr) {
                    console.error('写入文件时发生错误:', appendErr);
                } else {
                    console.log('数据已成功追加到 CSV 文件中');
                }
            });
        }
    });
}
function processTargets(targetList) {
    pb1.start(targetList.length, 0);
    const outputLogArray = [];

    targetList.forEach((targetItem, index) => {
        try {
            const targetFolder = path.resolve(miniprogram, fn.getFullSpellName(targetItem));
            fs.copySync(path.resolve(newbasecode), targetFolder);
            
            updateConfigFile(`${targetFolder}/project.config.json`, {
                appid: fn.getAppid(targetItem)
            });
            
            updateConfigFile(`${targetFolder}/project.private.config.json`, {
                projectname: encodeURIComponent(fn.getMiniProgramName(targetItem))
            });
            
            updateConfigFile(`${targetFolder}/app.js`, {
                miniId: fn.getAppid(targetItem),
                miniName: fn.getMiniProgramName(targetItem),
                appname: fn.getFirstSpellName(targetItem)
            });
            
            pb1.update(index + 1);
            outputLogArray.push(targetItem);
        } catch (error) {
            throw new Error(`复制出错: ${error}`);
        }
    });
    
    outputLog(outputLogArray);
    pb1.stop();
}
function updateConfigFile(filePath, replacements) {
    let fileContent = fs.readFileSync(filePath, 'utf8');

    for (const [key, value] of Object.entries(replacements)) {
        const regex = new RegExp(`(["']?${key}["']?\\s*:\\s*)(["']?)(.*?)(["']?)`, 'g');
        fileContent = fileContent.replace(regex, `$1$2${value}$4`);
    }

    fs.writeFileSync(filePath, fileContent);
}

/* function copyAndProcess(targetList) {
    pb1.start(targetList.length, 0)
    var output_log_array = []
    targetList.forEach((targetItem, index) => {
        try {
            fs.copySync(path.resolve(newbasecode), path.resolve(miniprogram, fn.getFullSpellName(targetItem)))
            // appid in project.config.json
            let configPath1 = path.resolve(miniprogram, fn.getFullSpellName(targetItem), "./project.config.json")
            let val1 = fs.readFileSync(configPath1).toString().replace(/(["']appid["']\:.*["']).*(["'])/, `$1${fn.getAppid(targetItem)}$2`);
            fs.writeFileSync(configPath1, val1)
            // projectname in project.private.config.json
            let configPath2 = path.resolve(miniprogram, fn.getFullSpellName(targetItem), "./project.private.config.json")
            let val2 = fs.readFileSync(configPath2).toString();
            val2 = val2.replace(/(["']projectname["']\:.*["']).*(["'])/, `$1${encodeURIComponent(fn.getMiniProgramName(targetItem))}$2`)
            fs.writeFileSync(configPath2, val2)
            // 4configs in app.js
            let configPath3 = path.resolve(miniprogram, fn.getFullSpellName(targetItem), "./app.js")
            let val3 = fs.readFileSync(configPath3).toString();
            val3 = val3.replace(/(["']?miniId["']?\:.*["']).*(["'])/, `$1${fn.getAppid(targetItem)}$2`)
            val3 = val3.replace(/(["']?miniName["']?\:.*["']).*(["'])/, `$1${fn.getMiniProgramName(targetItem)}$2`)
            val3 = val3.replace(/(["']?appname["']?\:.*["']).*(["'])/, `$1${fn.getFirstSpellName(targetItem)}$2`)
            fs.writeFileSync(configPath3, val3)
            pb1.update(index + 1)
            output_log_array.push(targetItem)
        } catch (error) {
            throw (`复制出错:${error}`)
        }
    })
    outputLog(output_log_array)
    pb1.stop()
} */

mainFlow();