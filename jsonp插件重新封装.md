import originJSONP from 'jsonp';

// 默认配置
const options = {
  // 示例回调函数
  callback: () => console.log('jsonp-userinit')
};

// JSONP 请求函数
export function jsonpGet(params, endpoint) {
  const baseUrl = 'https://xxxx.com/';
  const url = `${baseUrl}${endpoint}`;
  return jsonp(url, params, options);
}

// 封装 JSONP 逻辑
function jsonp(url, data, options) {
  const fullUrl = `${url}${url.indexOf('?') < 0 ? '?' : '&'}${serializeParams(data)}`;
  
  return new Promise((resolve, reject) => {
    originJSONP(fullUrl, options, (error, response) => {
      if (error) {
        reject(error);
      } else {
        resolve(response);
      }
    });
  });
}

// 序列化参数为查询字符串
function serializeParams(data) {
  return Object.keys(data)
    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(data[key] || '')}`)
    .join('&');
}
代码解释
jsonpGet 函数：接收参数和 API 端点，构建完整的请求 URL，并调用内部的 jsonp 函数。
jsonp 函数：处理请求的核心逻辑，生成完整的 URL 并返回一个 Promise。
serializeParams 函数：将参数对象转换为 URL 查询字符串格式，确保所有值都被正确编码。
这种重构使得代码更加模块化和易于理解，方便后续维护和扩展。