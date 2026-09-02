import rclpy
from rclpy.node import Node

from tf2_ros import Buffer, TransformListener
import time


class TCPReader(Node):

    def __init__(self):
        super().__init__('tcp_reader')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        time.sleep(2)

        self.timer = self.create_timer(0.5, self.read_tcp)


    def read_tcp(self):

        try:
            transform = self.tf_buffer.lookup_transform(
                'world',
                'dummy_tcp',
                rclpy.time.Time()
            )

            x = transform.transform.translation.x * 1000
            y = transform.transform.translation.y * 1000
            z = transform.transform.translation.z * 1000

            print(
                f"\rTCP Position: "
                f"X={x:.2f} mm  "
                f"Y={y:.2f} mm  "
                f"Z={z:.2f} mm",
                end=""
            )

        except Exception as e:
            pass


def main():

    rclpy.init()

    node = TCPReader()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
