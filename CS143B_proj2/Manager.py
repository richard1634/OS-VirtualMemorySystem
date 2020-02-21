
class Manager:
    def __init__(self):
        self.pm = [0] * 1024 * 512
        self.disk = [[0]*512]*1024
        self.bitmap = [0] * 1024
        #pages 0 and 1 are always occupied by ST
        self.bitmap[0] = 1
        self.bitmap[1] = 1
        ########################################
    # def init_pm(self,line1,line2):
    #     #Line 1 and 2 are prob list
    #     line1 = list(zip(*(iter(line1),) * 3))
    #     line2 = list(zip(*(iter(line2),) * 3))
    #
    #     for line in line1:
    #         # Segment table - tuple (8 4000 3)
    #         segment_num = int(line[0])
    #         size = int(line[1])
    #         frame_num = int(line[2])
    #         #size
    #         self.pm[2*segment_num] = size
    #         self.pm[2*segment_num+1] = frame_num
    #     for line in line2:
    #         # PT - 8 5 8 page 5 of seg 8 resides in frame 8
    #         segment_num = int(line[0])
    #         page_num = int(line[1])
    #         frame_num = int(line[2])
    #         frame = self.pm[2*segment_num+1]
    #         self.pm[frame*512+page_num] = frame_num
    #
    # def translate(self,va):
    #     #va into s, p ,w and pw(offset into segment and must not exceed segment size))
    #     s = va >> 18
    #     w = va & 511  # and with "1 1111 1111"
    #     pre_p = (va >> 9)
    #     p = pre_p & 511
    #     pw = va & 262143
    #     if pw >= self.pm[2*s]:
    #         print("error; VA i outside of segment boundary")
    #     else:
    #         PA = self.pm[self.pm[2*s+1]*512+p]*512+w
    #         print(PA)


#--------------------------Demand Paging---------------------------
    #todo - init disk, read block, translation
    #does init really work
    def init_pm(self,line1,line2):
        #could be  negative so bit map should be set to free or allocated
        #Line 1 and 2 are prob list
        line1 = list(zip(*(iter(line1),) * 3))
        line2 = list(zip(*(iter(line2),) * 3))

        for line in line1:
            # Segment table - tuple (8 4000 3)
            segment_num = int(line[0])
            size = int(line[1])
            frame_num = int(line[2])
            #size
            self.pm[2*segment_num] = size
            self.pm[2*segment_num+1] = frame_num # - pos
            self.bitmap[self.pm[2*segment_num+1]] = 1
        for line in line2:
            # PT - 8 5 8 page 5 of seg 8 resides in frame 8
            segment_num = int(line[0])
            page_num = int(line[1])
            frame_num = int(line[2])

            st_frame = self.pm[2*segment_num+1]
            if st_frame < 0:  #segment is not resident
                self.disk[abs(st_frame)][page_num] = frame_num
            else:
                self.pm[st_frame*512+page_num] = frame_num # - poss
                self.bitmap[self.pm[st_frame*512+page_num]] = 1  #AM I DOING BITMAP RIGHT

    def find_ff(self):
        for i in range(len(self.bitmap)):
            if self.bitmap[i] == 0:
                return i

    def translate(self,va,file):
        #va into s, p ,w and pw(offset into segment and must not exceed segment size))
        f = open(file, "a")
        s = va >> 18
        w = va & 511  # and with "1 1111 1111"
        pre_p = (va >> 9)
        p = pre_p & 511
        pw = va & 262143
        if pw >= self.pm[2*s]:
            f.write("-1 ")
        else:
            if self.pm[2*s+1] < 0:  #PT not resident
                #Allocate free frame f using list of free frames
                #Update list of free frames
                #Read disk block b = |PM[2s + 1]| into PM staring at location f*512: read_block(b, f1*512)
                #PM[2s + 1] = f   /* update ST entry */
                f1 = self.find_ff()
                self.bitmap[f1] = 1
                disk_block = abs(self.pm[2*s+1])
                self.read_block(disk_block,f1 * 512)
                self.pm[2*s+1] = f1

            elif self.pm[self.pm[2*s + 1]*512 + p] < 0: #Page is not resident
                #Allocate free frame f using list of free frames
                #Update list of free frames
                #Read disk block b = |PM[2s + 1]| into PM staring at location f*512: read_block(b, f1*512)
                #PM[PM[2s + 1]*512 + p] = f          /* update PT entry */
                f1 = self.find_ff()
                self.bitmap[f1] = 1
                disk_block = abs(self.pm[self.pm[2*s + 1]*512 + p])
                self.read_block(disk_block,f1 * 512)
                self.pm[self.pm[2*s + 1]*512 + p] = f1

            #return
            PA = self.pm[self.pm[2*s+1]*512+p]*512+w
            f.write(str(PA) + " ")
        f.close()

        #    print(PA)

    def read_block(self,b,m):
        for i in range(512):
            self.pm[m + i] = self.disk[b][i]


    # def write_block(self):
    #     pass
