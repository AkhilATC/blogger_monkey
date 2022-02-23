
# ⚙️ Netty's core components

1. Channels // Abasic construct of Java NIO
2. Callbacks // ChannelHandler callback channelActive()
3. Futures //
4. Events and handlers


> Echo-server client Impliemnatation

```
Server
- Define a class which extends ChannelInboundHandlerAdapter
- Override channelRead, channelReadComplete
Server Bootstrap
- Create a instance of server class
- define eventloop group -> EventLoopGroup g = new NioEventLoopGroup();
- define a bootstrap -> ServerBootstrap bt = new ServerBootstrap();
bt.group(eventLoop).channel(NioServerSocketChannel.class)
                    .localAddress(new InetSocketAddress(5000))
                    .childHandler(new ChannelInitializer<SocketChannel>() {
                        public void initChannel(SocketChannel ch){
                            ch.pipeline().addLast(netty_instance);
                        }
                    });
            ChannelFuture futureInst = bt.bind().sync();
            futureInst.channel().closeFuture().sync();
```

# ⚙️ Netty HTTP/HTTPS 
1. At first we define a request handler class that extends **ChannelInboundMessageHandlerAdapter<HttpRequest>**
Override messageRecived - The messageReceived method has access to the request and creates the response
**Note:** if you use SimpleChannelInboundHandler, then override channelRead0
2. A class that implements ChannelInitializer is also required to set up the pipeline. **ChannelInitializer<SocketChannel>**
3. A bootstrap group implimenation.
---
## ✍️ Netty server implementation 
A class with a main method instantiates and starts the server and a handler class is defined to process incoming requests:
```java
// Bootstap wraping
public class NettyHttpServer {

    public void startServer(String portNumber) throws InterruptedException {
        ServerBootstrap serverBtsp = new ServerBootstrap();
        serverBtsp.group(new NioEventLoopGroup(),new NioEventLoopGroup())
                .localAddress(Integer.parseInt(portNumber))
                .channel(NioServerSocketChannel.class)
                .childHandler(new JsonHandler());// Instance of your request handler
        serverBtsp.bind().sync().channel().closeFuture().sync();
    }
    public static void main(String[] args) throws InterruptedException {
        System.out.println("--- NettyHttpServer ---"+args[0]);
        new NettyHttpServer().startServer(args[0]);
    }
}
```
The handler class extends ChannelInboundMessageHandlerAdapter, which allows the class to be included in the server’s pipeline. The messageReceived method has access to the request and creates the response.
**Note:** In 4.1.73.Final you can use SimpleChannelInboundHandler<HttpRequest>

```java
public class NettyServer extends SimpleChannelInboundHandler<HttpRequest> {

    public void channelRead0(ChannelHandlerContext channelHandlerContext,
                                HttpRequest httpRequest){
                                /**
                                StringBuffer buf = new StringBuffer();
                                buf.append("{\"testResponse\":\"Hello World\"}"); // convert this as byte array
                                */
        byte[] byteArrray = "{\"testResponse\":\"Hello World\"}".getBytes();
        ByteBuf buf = Unpooled.wrappedBuffer(byteArrray);
        HttpResponse response = new DefaultFullHttpResponse(HttpVersion.HTTP_1_1,
                HttpResponseStatus.OK,buf);
        response.headers().add(HttpHeaderNames.CONTENT_TYPE,"application/json");
//        response.headers().add(HttpHeaderNames.CONTENT_LENGTH, buf.length());
        channelHandlerContext.writeAndFlush(response).addListener(
                ChannelFutureListener.CLOSE);


    }
}
```
---
```java
public class JsonHandler extends ChannelInitializer<SocketChannel> {

    public void initChannel(SocketChannel sc){
        ChannelPipeline pipeLine  = sc.pipeline();
        pipeLine.addLast("decoder", new HttpRequestDecoder());
//        pipeLine.addLast("aggregator", new );
        pipeLine.addLast("encoder", new HttpResponseEncoder());
        pipeLine.addLast("chunkedWriter", new ChunkedWriteHandler());
        pipeLine.addLast("handler", new NettyServer());// handler instance
    }

}
```
