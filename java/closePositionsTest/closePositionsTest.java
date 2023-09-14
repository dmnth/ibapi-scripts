import com.ib.client.*;

public class closePositionsTest extends DefaultEWrapper {

  private EReaderSignal readerSignal;
  private EClientSocket clientSocket;
  protected int currentOrderId;

  public closePositionsTest() {
    readerSignal = new EJavaSignal();
    clientSocket = new EClientSocket(this, readerSignal);
  }

  public EClientSocket getClient() {
    return clientSocket;
  }

  public EReaderSignal getSignal() {
    return readerSignal;
  }

  public int getCurrentOrderId() {
    return currentOrderId;
  }

  public void incrementCurrentOrderId(int orderId) {
    orderId++;
    currentOrderId = orderId;
  }

  public static void main(String[] args) throws InterruptedException {
    closePositionsTest wrapper = new closePositionsTest();

    final EClientSocket m_client = wrapper.getClient();
    final EReaderSignal m_signal = wrapper.getSignal();

    // Connection Parameters
    String hostIP = "192.168.43.222";
    int port = 7496;
    int clientId = 1001;

    //! [connect]
    m_client.eConnect(hostIP, port, clientId);
    //! [connect]
    //! [ereader]
    final EReader reader = new EReader(m_client, m_signal);

    reader.start();
  //An additional thread is created in this program design to empty the messaging queue
    new Thread(() -> {
    while (m_client.isConnected()) {
      m_signal.waitForSignal();
    try {
      reader.processMsgs();
    } catch (Exception e) {
      System.out.println("Exception: "+e.getMessage());
    }
    }
    }).start();Thread.sleep(1000);

    int orderId = wrapper.getCurrentOrderId();
    Contract contract = new Contract();
    contract.symbol("BMW");
    contract.secType("STK");
    contract.exchange("SMART");
    contract.currency("EUR");

    Order order = new Order();
    order.action("BUY");
    order.orderType("LMT");
    order.lmtPrice(147);
    order.totalQuantity(Decimal.get(10));

    m_client.placeOrder(orderId , contract, order);

    Thread.sleep(1000); 
    m_client.reqPositions(); 
    Thread.sleep(1000); 
    m_client.eDisconnect(); 
  } 

  @Override public void currentTime(long time) {
    System.out.println(EWrapperMsgGenerator.currentTime(time));
  }
  @Override public void nextValidId(int orderId) {
    System.out.println("OrderID: " + orderId);
    this.currentOrderId = orderId; } 

  @Override public void error(int id, int errorCode, String errorMsg, String advancedOrderRejectJson) {
    String str = "Error. Id: " + id + ", Code: " + errorCode + ", Msg: " + errorMsg;
    if (advancedOrderRejectJson != null) {
      str += (", AdvancedOrderRejectJson: " + advancedOrderRejectJson);
      }
    System.out.println(str + "\n"); 
  } 

  @Override public void position(String account, Contract contract, Decimal pos, double avgCost) {
    boolean posIsZero = pos.isZero();
    int position = Integer.parseInt(pos.toString());
    System.out.println(position);

    int orderId = this.getCurrentOrderId();
    
    System.out.println(contract);
    if (!posIsZero && avgCost>0) {
      Order order = new Order();
      if (position > 0) {
        order.action("SELL");
      }
      if (position < 0) {
        order.action("BUY");
      }
      order.orderType("MKT");
      order.totalQuantity(pos);
      this.incrementCurrentOrderId(orderId);
      System.out.println("Placing an order");
      this.getClient().placeOrder(orderId, contract, order);
      this.getClient().reqCurrentTime();
    } 
  } 
  @Override public void positionEnd() {
    System.out.println("Position End: " + EWrapperMsgGenerator.positionEnd());
  }
  }
