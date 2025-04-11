# Sử dụng Node.js làm base image
FROM node:18

# Thiết lập thư mục làm việc trong container
WORKDIR /usr/src/app

# Sao chép package.json và cài đặt dependencies
COPY package.json ./
RUN npm install

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Build ứng dụng Next.js
RUN npm run build

# Kiểm tra thư mục .next
RUN ls -la .next

# Expose cổng 3000
EXPOSE 3000

# Chạy ứng dụng ở chế độ production
CMD ["npm", "start"]