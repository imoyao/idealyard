import CryptoJS from "crypto-js";

const secretKey = '8M0jMkkyqkNrZGCZ3bL'

export function encryptFunc(rawStr) {
  return CryptoJS.AES.encrypt(rawStr, secretKey).toString();
}

export function decryptFunc(secretStr) {
  return CryptoJS.AES.decrypt(secretStr, secretKey).toString(CryptoJS.enc.Utf8)
}
