import zlib

ICON_DATA = b'\x00\x00\x01\x00\x01\x0003\x00\x00\x01\x00\x18\x00p\x1e\x00\x00\x16\x00\x00\x00(\x00\x00\x000\x00\x00\x00f\x00\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x87@P\x8aEL\x88CH\x88GI\x88HJ\x89JK\x86FG\x88HK\x89IK\x89GJ\x8aGK\x8bHL\x89HJ\x89IJ\x86FG\x86FG\x8aHI\x8fQJ\x8bUB\x8eXD\x8eYE\x8cXC\x8dXD\x8cWC\x8fZF\x8eYD\x8cVB\x91[F\x8eYD\x8dWB\x8cWA\x8dXB\x8fZD\x8eYC\x8cV@\x90YD\x8eWA\x8dWA\x8fZD\x8eYC\x8dYC\x8e[E\x8fXD\x8dWA\x8eYC\x8cX@\xa4\x8d\x83\xd3\xd2\xd2\x7f;\\\x809Q\x86?U\x91O_\x85BL\x9b^e\x8cMR\x8bJM\x93UV\x8bJM\x9b]_\x88GJ\x96Y[\x8aMO\x8cMO\x9b_b\x8aIJ\x9acV\x92]H\x91]H\x96dP\x8eZF\x9cmX\x8e[F\x94aN\x92^K\x91[G\x9djU\x8dXC\x9emZ\x93_I\x8eZE\x98eP\x90[E\x9cjS\x8c[A\x9dlQ\x99jN\x8c]B\xa0qV\x8d_C\x98kN\x90`D\x97hJ\x9akO\x90`D\xae\x97\x88\xd3\xd2\xd2q/X`!A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x89FV\x85DN\x86DJ\x8aKL\x8bIJ\x91RT\x8aIK\x8aIL\x85FI\x89JLyCE\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7fO=\x95cLrL5\x00\x00\x00\x00\x00\x00M4\x1e\x92gA\x8dd9\x8ef=\x00\x00\x00\x00\x00\x00\x00\x00\x00yV2\x92k@\x8dd9eH(\x00\x00\x00\x00\x00\x00vi\\\xd3\xd2\xd2i)T`!F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x83:P}4I\x84>M\x8bGQ\x87EI\x8bHJ\x87DE\x8eMN\x8aLM\x82BDr;=\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x82V8\x93e<rO+\x00\x00\x00\x00\x00\x00N7\x1c\x90j=\x90i;rP*\x00\x00\x00\x00\x00\x00\x00\x00\x00cH%\x97rB\x94o;bG \x00\x00\x00\x00\x00\x00shX\xd3\xd1\xd2\x8dc~\\\x1eE\x00\x00\x00\x00\x00\x00\x00\x00\x00\x92Hb\x827N\x89DW\x91Qc\x84>L\x9aW^\x89GI\x9b]^\x91UV\x88GJ\x80MP\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x82\\5\x9euJuS-\x00\x00\x00\x00\x00\x00O8\x1d\xa3\x82S\x92q8_K#\x00\x00\x00\x00\x00\x00\x00\x00\x00E7\x16\xa2\x88N\x97x=eO#\x00\x00\x00\x00\x00\x00yp[\xd3\xd1\xd2\xa6\x90\xa0T\x12>\x00\x00\x00\x00\x00\x00\x00\x00\x00y1P\x816Q\x817N\x818N\x839N\x86@O\x8cIN\x8aIK\x86HI\x88GJq;=\x00\x00\x00\x00\x00\x00\x00\x00\x00\x8cXB\x8eZF\x8eYF\x8fZF\x8d[B\x90cA\x92f>\x91f<\x91h>\x90h=\x8fh<rT+\x00\x00\x00\x00\x00\x00Q?\x1c\x8fs3\x91u33\'\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0e\n\x02\x8fx7\x92y3cS\x1f\x00\x00\x00\x00\x00\x00tmV\xd3\xd2\xd2\xcb\xbf\xc7Z%H\x00\x00\x00\x00\x00\x00\x00\x00\x00\x8eHi}2S\x81;S\x88FY\x808N\x98Vf\x88EP\x91RW\x8aLO\x8bJN~JM\x00\x00\x00\x00\x00\x00\x00\x00\x00\x8e]G\x99iU\x8cXD\x99jT\x8c_?\x9fxP\x9arI\x92g>\x9ewQ\x8eg;\xa2~Pw^/\x00\x00\x00\x00\x00\x00N>\x19\x94\x80?\x86q.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x89z9\x92\x811g[$\x00\x00\x00\x00\x00\x00vqV\xd3\xd2\xd1\xd1\xce\xd0eDY\x00\x00\x00\x00\x00\x00\x00\x00\x00z/Tw*Oz0K\x7f7L\x827M\x829M\x85>N\x88EL\x85DH\x88HKp:<\x00\x00\x00\x00\x00\x00\x00\x00\x00\x8aV@\x8cXD\x8dYD\x8f_D\x8fc>\x92kA\x8de;\x92i>\x93o@\x91q5\x91s6qZ\'\x00\x00\x00\x00\x00\x00OB\x17\x91~0te#\x00\x00\x00\x00\x00\x00,(\x08\x00\x00\x00\x00\x00\x00jc#\x8d\x84)d]\x1c\x00\x00\x00\x00\x00\x00tqU\xd3\xd2\xd2\xd3\xd3\xd3\x8c{\x87\x00\x00\x00\x00\x00\x00\x00\x00\x00}2Xp"J~4S\x8aE]\x815K\x88>T\x807K\x93RZ\x8ePR\x84DD{EF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x93_I\x98eP\x8cYB\x99nN\x92hA\x93kB\x96oE\x8fg8\x97wC\x8et4\x99~Dt`,\x00\x00\x00\x00\x00\x00PE\x17\x99\x89?]T\x1c\x00\x00\x00\x00\x00\x00mi\x1c\x00\x00\x00\x00\x00\x00MJ\x18\x95\x901b_\x19\x00\x00\x00\x00\x00\x00wvV\xd3\xd1\xd2\xd3\xd3\xd3\xa8\x9f\xa6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00*\x0c\x15\x93R^\x8fRU\x88EEyCD\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x85k;\x8ft3\x9f\x85Fyg*\x00\x00\x00\x00\x00\x00OH\x15\x9f\x95?:7\x0c\x00\x00\x00\x08\x08\x01\x89\x8a%::\x11\x00\x00\x00\x18\x18\x03\x93\x98-bg\x19\x00\x00\x00\x00\x00\x00yyV\xd3\xd2\xd2\xd3\xd3\xd3\xb3\xaf\xb3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00+\r\x16\x83=K\x88FH\x8aHHr;<\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00~f2\x90v3\x92|-te"\x00\x00\x00\x00\x00\x00PL\x12\x89\x86#\x00\x00\x00\x00\x00\x00AF\x0c\x90\x9b)[b\x17\x00\x00\x00\x00\x00\x00z\x87\x1f^j\x18\x00\x00\x00\x00\x00\x00svS\xd4\xd2\xd2\xd3\xd3\xd3\xb4\xb4\xb4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00+\r\x16\x8bIW\x8dMQ\x8aKK\x85ST\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x90yG\x91|1\x9e\x8e@uh%\x00\x00\x00\x00\x00\x00NN\x10\x7f\x82/\x00\x00\x00\x00\x00\x00gs \x8e\xa2&~\x8f1\x00\x00\x00\x00\x00\x00fz\x1fbu\x1e\x00\x00\x00\x00\x00\x00v~V\xd4\xd2\xd1\xd3\xd3\xd3\xb4\xb4\xb4\x00\x00\x00\x00\x00\x00\x00\x00\x00e\x1dMs(Rp$Nu\'N}2Q\x828O\x84:N\x81;J\x88EJ\x8bIJs;<\x00\x00\x00\x00\x00\x00\x00\x00\x00\x8dWC\x90`F\x91g?\x91g>\x90g;\x91p<\x8fr6\x90u6\x92{9\x94\x824\x90\x81.uj"\x00\x00\x00\x00\x00\x00PT\x12\\e\x15\x00\x00\x00\x00\x00\x00x\x90"\x89\xa7(\x84\xa0)\x00\x00\x00\x00\x00\x00I[\x13]u\x1b\x00\x00\x00\x00\x00\x00p}T\xd4\xd1\xd1\xd3\xd3\xd3\xb4\xb4\xb4\x00\x00\x00\x00\x00\x00\x00\x00\x00u5cj$Pz6]\x84Aew/P\x8bG]\x809M\x90O_\x92SY\x89HJzHH\x00\x00\x00\x00\x00\x00\x00\x00\x00\x96bN\x98kN\x93iA\xa3zR\x92l=\x99{E\x99}G\x90t:\x9e\x88K\x91\x815\x9f\x92Gzt+\x00\x00\x00\x00\x00\x00OV\x15BK\x1a\x00\x00\x00\x10\x17\x03\x89\xaf<\x89\xb3<\x8f\xbaH3G\x12\x00\x00\x00\x19%\x07Yx%\x00\x00\x00\x00\x00\x00n\x81Y\xd3\xd1\xd2\xd3\xd3\xd3\xb4\xb4\xb4\x00\x00\x00\x00\x00\x00\x00\x00\x00o(Wg\x19Hx-U{6Zu(M\x86:S\x815J\x8aDV\x8bKS\x83DGt>@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x8cXB\x93fF\x91h>\x98oF\x8ei8\x98z@\x91u8\x92{7\x9b\x88C\x8f\x801\x94\x8c1qp\x1f\x00\x00\x00\x00\x00\x00BL\x10\x04\x05\x01\x00\x00\x00A^\x1a\x84\xbcB~\xb9?\x80\xbdGPy*\x00\x00\x00\x00\x00\x00<Y\x1a\x00\x00\x00\x00\x00\x00m\x84Y\xd3\xd1\xd2\xd3\xd3\xd3\xb4\xb4\xb4\x00\x00\x00\x00\x00\x00\x00\x00\x00f\x1eNh\x1cNn#Lr)Nu*Q\x84:W\x839O\x829N\x84AK\x88JMt?B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x91^F\x94kG\x8df<\x92k@\x90p;\x90t8\x93w<\x90y3\x93\x816\x91\x832\x96\x904uu$\x00\x00\x00\x00\x00\x00\r\x12\x01\x00\x00\x00\x00\x00\x00W\x8e8r\xc2Vr\xc5Wx\xc6\\_\xa0D\x00\x00\x00\x00\x00\x00\n\x16\x04\x00\x00\x00\x00\x00\x00i\x85\\\xd4\xd1\xd2\xd3\xd3\xd3\xb4\xb4\xb4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x03\x05\x8cIU\x8dNR\x85RT\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00;3\x15\x94\x872\xa4\x9dGz{*\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00d\xb8ec\xd3\x81a\xd2}y\xd6\x81g\xc4c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00h\x88c\xd3\xd1\xd2\xd3\xd3\xd3\xb4\xb4\xb4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\t\x02\x03\x85@M\x89GJr:<\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x004.\r\x92\x880\x91\x8d*uy\x1e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\'\rI\xd5\x959\xdd\xb5?\xdb\xa7P\xd6\x8d[\xd3|&Y/\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00d\x89d\xd3\xd1\xd2\xd3\xd3\xd3\xb4\xb4\xb4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0b\x03\x04\x8fO[\x88IK|JL\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00=9!\xae\xa5y\xb1\xad\x82\x8b\x8cb\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00MsXz\xdf\xce>\xe6\xe3/\xdf\xc7L\xdf\xafL\xd9\x99B\x94d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00d\x8ej\xd3\xd2\xd1\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd0\xcc\xd0{Src\x19O]\x12Hq%Ps)Px.Q\x838R\x7f7J\x87CN\x84CE\x88GJ\x8cQH\x94\\J\x8eZG\x8c^?\x92kC\x8ed<\x91n=\x8dr6\x94w;\x94|7\x8f}-\x95\x88D\xc9\xc1\xa8\xd6\xd4\xd1\xd3\xd3\xd1\xd2\xd4\xd0\xd1\xd3\xd0\xd1\xd4\xd0\xd1\xd3\xd2\xd0\xd3\xd3\xbf\xd4\xd99\xe3\xe6(\xe1\xd16\xdc\xb8=\xdb\xa5M\xd9\x9dU\xd5\x8aR\xd3\x83Z\xd4\x87X\xd3\x85\x87\xc7\x98\xd3\xd2\xd1\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd2\xd3\xa8\x92\xa1^\x13Hh Sz2\\q\'Mw0T|5M\x88DW\x81?K\x8bKN\x92UW\x8aQG\x91]J\x8bVA\x94iH\x93kB\x91h>\x99zH\x91u9\x93w;\x93|8\x93\x826\x95\x87=\x95\x8aE\xcc\xc9\xb3\xd6\xd2\xd0\xd4\xd2\xd3\xd5\xd2\xd3\xd5\xd2\xd3\xd5\xd2\xd3\xd3\xd3\xd3\xc4\xd5\xd8D\xe4\xeb*\xe0\xd84\xe2\xc8;\xdb\xb1H\xdb\xa8H\xda\x9fS\xd7\x95]\xd5\x8bW\xd5\x87\x89\xc9\x9d\xd3\xd2\xd1\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xc4\xbc\xc3`!Lk%U~:es(Q\x80:]\x807O\x8fL_\x86ER\x8dLQ\x97^`\x8dTI\x96eQ\x8dYC\x96kJ\x98qJ\x92j?\xa0\x83R\x92v<\x94{A\x96\x81=\x95\x847\x9d\x8fI\x8f\x88-\x95\x92C\xc5\xc2\xa8\xd3\xd2\xd2\xd3\xd2\xd3\xd4\xd2\xd3\xd4\xd2\xd3\xd3\xd3\xd3\xc4\xd6\xdaI\xe5\xec0\xe2\xe1?\xe4\xcf6\xde\xc1L\xdd\xaeJ\xda\xa7L\xdb\xa9\\\xdc\xa4P\xd7\x8e\x87\xc9\xa0\xd3\xd2\xd1\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd2\xce\xd1uQha\x17Lg\x1cNt(Rs(N\x836Q\x827L\x86?O\x86DJ\x88GJ\x8cSH\x90ZG\x8dYB\x8ec>\x91j@\x8fi;\x90t:\x8es6\x91y7\x95\x806\x90~0\x8f\x854\x91\x8d/\x92\x900\x93\x95>\xc8\xca\xac\xd3\xd3\xce\\\\\\,,,nnn\xb0\xc0\xc19\xe4\xe8&\xe5\xe7)\xe1\xcd)\xe1\xc9<\xdc\xb5A\xdb\xa8=\xda\xa6<\xdc\xa5=\xdb\xa5{\xca\xab\xd3\xd2\xd1\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xaa\x96\xa1e\x1fRz5bt\'Q\x8aCi\x815Q\x93L_\x8fLY\x89HK\x9a^^\x8eUG\xa0nY\x91^D\x97mH\x9fzS\x90k;\x9e\x84N\x90v8\x9b\x86D\x98\x87@\x91\x835\xa0\x97J\x90\x8d-\xa0\x9eC\x93\x9c2\x8f\x9f;\xc1\xc9\xa4>>=\x00\x00\x00\x00\x00\x00.23A\xd5\xd9\'\xe6\xe97\xe5\xd3+\xe1\xcbF\xe3\xc4E\xdb\xa9D\xdd\xa9J\xde\xadA\xda\xa7\x80\xcd\xb2\xd4\xd2\xd1\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd2\xd4\xbf\xb7\xbdb\x1eMi\x1cOs%Qq%M~2O\x849M\x87@K\x87EH\x89IJ\x90WH\x8cYD\x8dY=\x95g@\x93iA\x91l:\x93u:\x93v7\x90|5\x8e\x7f2\x91\x831\x95\x8d3\x90\x8e,\x8f\x94)\x8e\x9b(\x8c\x9f)\x95\xaeG\xb9\xc5\xa4\xcf\xcf\xcd\x9b\x9a\x9a\x00\x00\x00\x19ru&\xe4\xea#\xe1\xd0\'\xe0\xcc0\xdf\xc3>\xda\xa9@\xdc\xa6?\xdb\xa6@\xdc\xa7{\xcb\xae\xd1\xd2\xd1\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd2\xd2\xd3\xd1\xcd\xd2\x86`yp+Yr%P\x87@f\x7f4R\x88BV\x87DO\x8aJN\x94Z[\x8eVF\x9dlX\x93bF\x93i?\x94pF\x93p:\xa0\x84H\x90t3\x9d\x8aC\x97\x89>\x8f\x84.\x9c\x94?\x90\x8f*\x9d\xa4?\x89\x9b)\x90\xa9/\x90\xaf>\x8c\xb3E\xbd\xcf\xa9\xd2\xd3\xcfktv\x00\x00\x00#\xbc\xc1:\xe4\xd5)\xe0\xcb>\xe1\xc7I\xdc\xacC\xdb\xa6M\xde\xadB\xdb\xa9\x7f\xcc\xb0\xd2\xd2\xd1\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd4\xd3\xd3\xa1\x90\x9em%Wm M|0W\x804R\x84;P\x86BL\x89IL\x90VT\x8eVE\x92^J\x92bB\x91f>\x94jB\x94q:\x97{@\x8et4\x99\x87=\x95\x868\x8e\x87+\x94\x8f6\x8e\x91)\x96\xa05\x8e\xa2.\x8a\xa6\'\x8f\xb4>\x82\xb9?\x89\xc4a\xb7\xd4\xb8\xb0\xc2\xc3\x00\x00\x00\t]]3\xe0\xce,\xe0\xcb:\xdf\xbfC\xd9\xa8E\xdb\xa9G\xdb\xa9C\xdb\xaa}\xcc\xaf\xd3\xd2\xd1\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3~~~\x00\x00\x00B\x144o#Ps)O}2K\x83<N\x89GO\x83BE{CA\x00\x00\x00?&\x1c\x8b]<\x92iA\x88e>\x00\x00\x00.$\x0e\x90x8\x8e\x7f3\x8b\x7f0\x93\x8c.\x93\x8f6]`\x19\x00\x00\x00j|\x1b\x8b\xaa,\x85\xb34|\xbeEq\xc8`[\xd3\x94\x8f\xd9\xd0\x03!"\x00\x00\x00#\xb4\xa3,\xe1\xc9?\xdd\xb4D\xda\xa9?\xd9\xa7F\xdc\xa9=\xdb\xa7z\xca\xad\xd3\xd2\xd1\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\x9d\x9d\x9d\x00\x00\x00F.>t1S\x89Fd\x81;O\x8fP^\x87LP\x89JL\x95^Y\n\x04\x02\x12\n\x06\x8ca>\x97pH\xa0zR!\x18\x07\x00\x00\x00\x89q4\x9b\x8bD\x95\x89A\x91\x8a0\x9d\x97Fqu"\x00\x00\x00Xg\x1e\x8b\xac4\x8e\xbbMx\xbeLw\xcfwM\xd7\xa1A\xd5\xc9\x00\x00\x00\x00\x00\x00\x12TJ9\xda\xb7X\xe0\xb1P\xdb\xaaF\xda\xa9P\xdd\xacE\xda\xa6\x7f\xcd\xb0\xd2\xd2\xd1\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xb6\xb6\xb6\x00\x00\x00\x1d\x0f\x16}4O\x94Og\x8aBU\x92S]\x8dPT\x85DE\x8cRG;#\x19\x00\x00\x00\x81[9\x90g=\x90i>J:\x1a\x00\x00\x00{f*\x91\x812\x8d\x820\x92\x8c,\x90\x8d/\x84\x8b\'\x00\x00\x007B\x0b\x89\xab-\x85\xb45y\xbeGl\xc7dN\xd7\x94*\xbe\x9d\x00\x00\x00\x04&\x1d\x00\x00\x00-\xaa\x80A\xdc\xa6A\xdb\xa6@\xdb\xa6A\xdc\xa6?\xdb\xa7x\xca\xad\xd2\xd2\xd1\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xcc\xcc\xcc\x00\x00\x00\x00\x00\x00z3I\x94Pd\x89CQ\x98Z_\x91UX\x8dOO\xa3ocY7*\x00\x00\x00tT5\x96oE\x97uHcO%\x00\x00\x00hW$\x9b\x8b>\x94\x898\x95\x90/\xa3\xa1F\x8e\x98&\x15\x18\x03\x03\x05\x00\x89\xa90\x8e\xbbD}\xbdE~\xcdj^\xd1}=\xa8r\x00\x00\x00.\x9fu\x03\x17\x0f\x0fF2L\xdb\xa5K\xdb\x9fS\xdb\x9f^\xdc\x9fP\xd6\x92\x83\xca\xa1\xd3\xd2\xd1\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3POO\x00\x00\x00j,=\x85?M\x88EL\x86HK\x88KN\x82GD\x8eZIlD4\x00\x00\x00eJ3\x92kA\x8fp@u^+\x00\x00\x00L>\x17\x95\x847\x8d\x83-\x93\x8e-\x94\x924\x92\x99+AI\r\x00\x00\x00t\x90!\x89\xb49~\xb9?u\xc1Qi\xcag;\x8bR\x00\x00\x00G\xbbu3\x8aY\x00\x00\x00?\xa0gS\xd3\x87W\xd5\x88Z\xd5\x89U\xd3\x85\x84\xc7\x9a\xd1\xd3\xd0\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\x7f}}\x00\x00\x00\\+2\x8fNR\x85FI\x90RV\x86IK\x8aRJ\x96dR}N?\x00\x00\x00F/\x1d\x9cuP\xa2\x80\\\x8am=\x00\x00\x00&\x1e\t\x93\x837\x95\x8b9\x91\x8b-\x95\x918\x91\x98+aj\x1d\x00\x00\x00e}\x1f\x8b\xb48\x82\xb7=\x80\xc3Ur\xc9_3k5\x00\x00\x00U\xc8|Y\xcc\x84\x08!\x11\x13:"U\xcf\x83U\xd4\x86Y\xd5\x88W\xd4\x85\x88\xc9\x9a\xd0\xd2\xd0\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\x9f\x9e\x9e\x00\x00\x00G"%\x97X[\x8aIM\x8ePS\x89LJ\x90XJ\x96hU\x88UC\x00\x00\x00\x1a\x0f\x06\x96nD\x9auM\x8dj;\x19\x13\x07\x00\x00\x00\x96\x84I\x9f\x92I\x98\x906\x9a\x97<\x92\x9b,y\x83*\x00\x00\x00Rb\x16\x8f\xb2;\x84\xb57\x87\xc4Ww\xc1P A\x1c\x08\x18\x08c\xccqh\xda\x8b9\x8fX\x00\x00\x00=\x9a^Z\xd7\x88_\xd7\x8aV\xd5\x84\x86\xca\x9c\xd1\xd3\xd0\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xb7\xb5\xb5\x00\x00\x00!\r\x0e\x88HL\x89GI\x8bJL\x8bOJ\x8cUC\x8eZD\x91ZE2\x1d\x13\x00\x00\x00\x85^4\x91h=\x92m<C4\x17\x00\x00\x00m\\,\x96\x85@\x9b\x8e;\xa7\xa0T\x90\x95.\x83\x8b"\x00\x00\x00.6\x06\x8b\xaa*\x85\xb32|\xba>s\xb9E\x00\x00\x00&P#f\xc9bf\xcdj[\xc7o\x0c*\x16\x0e/\x19Q\xcd~W\xd5\x86V\xd5\x84\x85\xc7\x9a\xd0\xd2\xd1\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd2\xd2\xd2\xcc\xca\xca\x04\x02\x02\x00\x00\x00\x8eVY\x88JK\x99`b\x96^X\x8dYH\x9fq\\\x8eZE]>0\x00\x00\x00{Y6\x9bsL\x94o>kY5\x00\x00\x008-\x15\x9a\x88D\x94\x85:\xa0\x95M\x97\x94:\xa2\xa3H\x0f\x11\x02\x00\x00\x00\x96\xabC\x8a\xb3:\x8a\xc0Rm\xaaD\x00\x00\x00Ar:k\xcaft\xd1qk\xcbiQ\x93S\x00\x00\x00E\x90Qo\xd8\x8b^\xd2\x80\x8c\xc9\x9e\xd0\xd2\xd2\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd2\xcf\xcf6$%\x00\x00\x00p8<\x86FI\x8aKM\x8fTI\x8cWA\x8dZC\x8dYEg@/\x00\x00\x00dE\'\x90f>\x92n<q[-\x00\x00\x00\x00\x00\x00bV!\x90\x812\x92\x878\x91\x8e.\x90\x91(-0\x06\x00\x00\x00\x96\xaaA\x8e\xb29\x88\xb9Kd\x9a;\x00\x00\x00K\x86>h\xc8dj\xcbfj\xcagh\xc5d\x14/\x13\x0c"\x0bd\xc1df\xcah\x8d\xc4\x8d\xd1\xd3\xd1\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd1\xd2VDE\x00\x00\x00gGI\x84VY\x8caa\x8fd[\x8egW\x97sc\x8bdT\x83cT\x00\x00\x00Q=,\x9c|a\x90tO\x8cvS\x00\x00\x002*\x19\x0c\n\x04ZQ,\x91\x87S\x92\x8dI\x87\x86J\x04\x04\x01\x1a\x1c\x08\x9c\xacU\x96\xaaQ\xa1\xbbhg\x86D\x00\x00\x00Y\x98Gn\xcci{\xd4um\xcchr\xd1mL\x94I\x00\x00\x00H\x8aGk\xcdh\x93\xc7\x91\xd0\xd2\xd1\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xa0\x9d\x9d\x00\x00\x00nlm\xd0\xcc\xcc\xd1\xce\xce\xd1\xcd\xcb\xcf\xcc\xca\xd2\xcf\xcd\xce\xcc\xc9\xc6\xc4\xc1\x00\x00\x00;;:\xd0\xce\xcb\xce\xcd\xc8\xcd\xcb\xc8\x0f\x0f\x0e\\[Y\xae\xad\xa9--,\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x8e\x8f\x89\xd1\xd3\xca\xcf\xd1\xc8\xd0\xd2\xcb{~y\x00\x00\x00d\xaaXm\xccet\xd0oj\xcagm\xcdif\xc5b\x199\x19\t\x19\x08b\xbd`\x8e\xc3\x8d\xd0\xd2\xd0\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xba\xba\xba\x00\x00\x00111\xd2\xd2\xd2\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3>>>\x00\x00\x00\xc8\xc8\xc8\xd3\xd3\xd3\xd3\xd3\xd3XXX\x1a\x1a\x1a\xd1\xd1\xd1\xc5\xc5\xc5\x84\x84\x84>>>333\x88\x88\x88\xcf\xcf\xcf\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\\\\\\\x00\x00\x00l\xbbhg\xc9ci\xcbei\xcadm\xcckj\xccfJ\x96F\x00\x00\x00A\x7f?\x8e\xc3\x8d\xd0\xd2\xd1\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xcf\xcf\xcf\x10\x10\x10\x00\x00\x00\xc3\xc3\xc3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xcb\xd5\xcc}\xcdzk\xc9hu\xd0qn\xcbhy\xd3vp\xcdml\xcdgr\xd0nk\xcbi\x92\xc7\x92\xd0\xd2\xd2\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3ZZZ\x00\x00\x00\xac\xac\xac\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xca\xd3\xc9t\xc8pi\xcaek\xcbhj\xcbfi\xccei\xcceh\xcbcj\xccdk\xccf\x8d\xc2\x8b\xd0\xd2\xd2\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xcf\xcf\xcf\x08\x08\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00>>>\xd3\xd3\xd3\xbc\xbc\xbc\x00\x00\x00ggg\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xcd\xd6\xccy\xcbum\xcci{\xd4{k\xcbfp\xd1lk\xcbhn\xceju\xd3tl\xcbf\x91\xc5\x8f\xd0\xd2\xd2\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3WWW\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc8\xc8\xc8\xd1\xd1\xd1,,,\x1a\x1a\x1a\xcf\xcf\xcf\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xcb\xd4\xcas\xc8mj\xcbfn\xcckl\xcbel\xcbfj\xc9dl\xcdfn\xcdll\xcaf\x8b\xc1\x8e\xd0\xd2\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xcb\xd4\xc8v\xcdpe\xcb`j\xcefj\xcacr\xcflj\xccfg\xcbbj\xcddk\xccd\x8f\xc4\x91\xd0\xd2\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xcb\xd5\xcay\xcdue\xccak\xd1hi\xcccv\xd2qk\xcefe\xcc`k\xd0ff\xcca\x91\xc6\x92\xcf\xd2\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xd3\xc9\xd3\xc7s\xc9nj\xcbgk\xcbgk\xcbgl\xcbgi\xcacj\xcbck\xcbfj\xcae\x8e\xc0\x90\xcf\xd1\xd3\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc9\xc5\xca\xc3\xa2\xc3\x9f\x9e\xc2\x9e\xa2\xc7\xa2\xa0\xc3\x9f\xa1\xc5\xa0\x9f\xc3\x9e\xa1\xc5\x9f\xa3\xc7\xa2\x9f\xc4\x9c\xaf\xc4\xad\xd1\xd2\xd3\xff\xff\xff\xff\xff\xff\x00\x00\xff\xff\xff\xff\xff\xff\x00\x00\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

compressed_icon_data = b'x\x9c\xedX\x87WT\xd7\xd6\'\xd1\xe4\x99D\xa3\xd1g}jb\x07\xa4Ig\x06f\x98\xde+L\x05\x06d\x98\x0eH\x1b\x90\xde\x06\x98z\xe7\xde\x99\xa1\x08R,Q1\x96$\x9an\x8aQC\x99\xa1\xcc\x0ch\x14\x93\xe8K\xf9\xea\xff\xf0}\xe7:<\xe2S\x8cyk\xbd\x95o\xado\xbd\xcd\x9d\xcb9\xfb\xees\xef\xef\xee\xfd;\xfb\xecs\xc3\xc2^\x00\x7fq\ta\xe0\xbc%\xaclgX\xd8\xa6\xb0\xb0\xb0p\xf0\x8b\x03?uXH\xff/\xf9\xff!]\x99|+\x85m&\xd1\xcd4\x86\x99\xce\xb40Y\x9dT\x9a\x99\xce\xb20X\x16\x1a\xd3Jc\xd9\xe8l\x0b\xd03\x98@\x0f\x0e+\x9d\xe1\x140m""$%C2\x8a]JrH\xc9v\t\xc9)\xa7B2\xb2]LDr\xd0\x86CB\xb4K\x08\x0e)\xd1)\x07f$\xbb8\x13\x96\x91!\xa0\x91\x10B\x1a\x87\x8c\x04\xe5P\x9cR`I@\r\xa4\x99\xa7\x1d\xed\xc1@\xa0\x19\x9b\xdb\x92&\xe8\xc4\x8b\x10^~\x07\x91=\xa0P\xd99B\x1b\x93\xe3\x16\x89\xc1y /\xdfLc\xf6\xc8r\xac\x1c\x9e\x9d\xc3\x1b\xc8/\xb42\x98\xfdJ\xb1+\x8f\x8e\xe4\xd1{\x8a\xf8\x90\x9cz\xbcD\n\xe5P=\x87\xb9.\x05\x0b\xc9\xa1\r\xeaE\x0e)i\xa8D\xee\xceg@rJ\x9f\x8a\x0f\xe7P\x8e\xeb\xb3\xec9\x84\xc1b\xc11=\xd7\x9eG\x1c)\x17;\xf2I}\x06.\\@\xee\xd52\xfb\r<\xd0\xb8\xd4k\x06x\xcac\xa5\x05\xbb\x08K\xee\xb2P\xc5\x1ddn\'\x99ie\xb1m\x0c&"\xcc\xb62XV\x06\xbb\x83\xca\xb00\xd9\xb5$\xca\xef\xf1y3/\xa3[\xc9\xae`\'\x85\xba\x9c\xc4\x9d.\r\xc1Q\x94\x06\xa93\x96lj\xc5\xf1.C&P\xaa\xe8\xe1!M\xb5.\x17\xe0\xd1Ed\x17\xec\xa2.\x99\xb5c\xf8\x8d\x89\x0c\x13\x8ec\xa3\t\xba(\x0c\x1b\x9d\xd9E\xa6@\x1c\xae\x95\xcdi#\x92+\xb0\x19a\xbfC\xda\xc4\xa9nUz\x05\xef`\xa8\xcbM\xd9\x0e\xeb3`\x1d\xb6\x82\x1f\xb9d\xa3\xa4\xef\xeb\xad z\x8e`\x0bio\x854\x95Zi\xd0\x1fp(\x9brw\xfe\xfa\xd6.za[\n\xd7B\x96 \x02\xa5\t\xc7\xee\x97(,4\xc6@\x9e\x02\x11\x89A\xe0Z8\xfc\xdf\x85\'7i\xc8\xc84fE\x87\xba\xbc\xd4\x1d\xa7\xda\xb2\\\xe5\xa9\xf9\xac=K6\x94\x94M\'\xcd\xdc\xde\xa3\x19*\xde\xa2\xb2\xb6,\x07\xe09\x03\x8fd\xaf\xc7\xfd\xea\xc6C\xfc\xd6dAk\n\xb75\x95\xdb\x9e\xc6\xed\xcc\xe4\xd9\x19\\\x10\xb2N:\x03\xe0)\x7f\xcc?v)\x11B9L\x05Lv\xe4\x10a%\xc1\xa5\xc6!\xeatD\x8b\x83\xb5\x19NmzE\xf6\xa2\x7f\x04\xf8\xed\xce\xca\x04\xc4\x98\x90p`\xf5\xd2\xf0\xd7_}\xd1y4\xc5U\x9b\xa0\xccz3\xa4\xa9*\x11\x83xy\xbf\x1c\x93\xef\xa3/\x99At]c|V+6\xcbL\x95\xb5\xa4r\xfb\xc4j3\x85\x8f\x08%V6\xcf\xc6\xe4619\xbfZ\xe6\xd1\x8e\xe9Dv)\xf9\x98>\xdb\x9e\x8f\x1f>\xca\xef\xaf`\xb84\xb8\xa1\x1a\x01\xa4\xc1\x9el\xe2\xd7(b\x17\xe3\x85\xdb\xeai\xc1w\x96\xc7<\xe1FK]\x9a\xab\xf5\x90&go\xa8[]\x0e\xf0\xf8\xfd\xd3\xb3*\xb2l\xc9\xa6.6\xbb&\x92W\x17\xc7jNa\xb7\xa5p\xda\xd28\x1d8\xae\x99\xc2\xee \xd3A\x12(\xc3\xa4/YZ\xc5\x99\x00\x8cCFv\xe6\x93\x9dJ\x9c\xcb@p\xa8\xb0.\x1d\xce}$\x13)OB*\x93\xcb\xe5\x07\x16\xe3E\xdc\x8c4\xc5U\xa9\x16\xe3\x12\x15\xbe*\xd4\xd0+\xf78L\x11Ey\xdb\x17\xfdS.\x02\xfe\t\x06\x83\xf6\xfa\xae\xa5\xa74\xc6K\xcbv3\x9b\x12\xb3\xac\x94\xbc\xd6$\x96\x19\x97\xdd\x92\xc2r\x0b\xe5\x10_h"\x93\xeb)\xbf2\x1fLg0\x97\xed2\xe2\xb1R\xaeKKp\x1b\x88=G(NMjo\r\t\xaaJ<\xd6D\xae*\x88\nY\xf2)\x9b\x8fY\xf0y\xd9\x8b\xcf-\xd1-68\xcc-\xdd\xf0\xa1\xc2\xfc\xad\xa1nM\xb5\x18\xf0\x07\xe097|&\xec\xd9\x12\xb9z\xa3[\xa8p\nEf\n\xa5\x96D\xfe\r\xcb\x90t\x18\xb0\xce\xaa\x84\xe1\x0ej\xadfq6\xf1\xe8\x1b\x87\xbb\xf1\x98\x14\x94<\xabV\xbd`\xb1\xee\xc3`\xde\x00\xed-[V\xb8\xfb\xa2\x0b5\x8bxjk\xc5!\xff\\\xb9|\xe57\xee\x7fp\xcd\xa6\xf6\x0c\x96\x99J\xb7\xd2\xe9\x15\xd8\xf4\xdf\xb0\x0cI\x93:\x1e\xaeNp5DW\xa9v\x874|\xf6zK\xe7b\xb0\x08\xd4\xd5\xf0@DN\xe1\xe6P\xb7\xae\xebM\x85~q\xb1\xaf\xac\xce\x9a{\x84\xe7\xea\xd5\xab\xbf\x8d\xc7\xc6\x9088\x02+\x8b\xd5\x91\x95\xfd\\<p-\ri84\x04e\x1a\xb5\xfbB\x1a.w]s\xdb"\xb75\x95oA\'\xf779\x0f\x85\xba\xea\xba7\x0b\x8d;C\xed\xea&\xf1\\\xc0\xff\x04\x1e\xd5\x0eNe\xb8\xb0l/\xd7x\x80\xdb\x18/hK\xe5\x990\xdcV,\xd3La\x82t]\xf9\x98\x7f\x1c\x12\x12\\@E4xD\x83\x835X\xa4,\xddY\x91\x0c\x1b\x93]\xf5i\x9e\xb6D\xb85\xc6\xa8\xff\x9b\x7f\xb2\xd7\xe7\xaa6\x86\xdaG\xe1\xdd\x96\xb3\xe1\xa6\x91\x88P\x97\x91\xb3!\xcf\xf8\x97P\xbb\xac1{\xce\xff$\x1ec\x92R\xbf\x97_\x97\x9cg"\xa8jb\xf96Z^K\x1a\x07\xe6\xe5\xbb\xb2d`U\xad\xa3\xff\x9a\x19z\n\xb9`\x01r\xeb\x08\xa7\xea\x84\xae\xe2\x8cc\xf5\x94c\x8d4\xb8\n3df!\xadI\xc3.Z]\xd5b\xfe\xe1\x897\x12Y\xdb@c\xdd\xe6\x15\x96\xcb\xe9\x96+\xe9\xceO\xe9\t\xb4\xf5@\xb3u\xdf\x9fdG\x17\xddX\xda*\x0b\xf1\xf9q<G\xc2%\x9a\xad\xf4\xa3\xd1\xa2\xfad\xb91\x9c\xd3\x89\xc9jMbZ\xc9b\x1b+\xab\x9dL\xab\xc2e.Y\x82|\xe8VSA\xf6\xeb;B\x85t\xa9}u\x99\x881\xd5U\x9f2`&9[\x0ey\xec\x87\xca\xcb\x16\x13\x1d\x91\xbdn\xe5K/\x80\x06A\xb1\xcdt\x8d\xd8\xf4\t\xbe\xe5s\x1a\xbfv\x91\xed\xe9\xb2m\xa1F\x89i\x19<\xea\x9d\\\xedvn\xe9\x1evE\x04\xd7\x18)0a$\xedi\xbc\xb64\xae\x89\xc0239Ux\xe2\x92%\xa2\xa0z\x0c4\x87:\x1d,\x8bp\x19\x16\xaeJu\xd7\xa4\xc3\xb5\t\xee\xd6d\xa4=\xbe\x07N4\x1a\x17\x13\xdd\x9a\xf5/\x84\x1a\x12(\xb5\xe2kq\xc5-\xc9\xd1or\xf3G\x16\xa7\xea\xab\x9bV\x86\x1a\xba\x8e\xdc\xb9\xa7\xf0,+\xabW\xbcdg\x88\x1c\\a\x87\xf0\xf9|\xc6&l\xf4t\xc5\x9f\x1e\xa4\xd5\xd5G>q\xa9\xe8c\x952\xd8z8\xd0X{\xbbUsS\xf9\xc4U\xadY\xf9\xb4\x7f\x96\x95W^\\\xd1\x91\xc9\x01\xe5Y\x05\xe6\xf9\xf3=1f\x8d\xcb\x1c\x878"\x8d\xb5;\x1f\xd7\xaf;\xb0\x861\xdf\x9d\xf6\xdd\x07\xf8\x85\xb3\xfc\xdb\x8e\x9c`\xc3~Y\xec\xdf\xa1\xb5\x14\xfdN<\xaf\xadX\xe9\xe4\xe5\x98\x19\xac\x06&\xfb\xb9x2\xd2v]z\xbb\xf6\xbd\x8bm6{\xe1\xe3zN\xa5\xb4\xee\x87i\xdc/?\xc6\xfe0\xc6\xfe\xe12\xfb\xee1\xa2\xa7\xe8\xef\xf0@\xfa\xe0\xa3\xf9\xbe$\xb3\xbe\xd9\xfa\xac\n\xe5V^\xdezz\xf9>~e\x04\xffh\x8c\xa0=U\xd8\x9c\xc2\xec"qM$\nX\xe2\xed\x02\xba\'\x97\t\xc9iv\x05\xdee AE\xe9Hi\x86\xa3"\xd9S\x83\xf54\xa48\x1b\xa3\xbb\xcd\xe4\x89\xeb\xe7n\xcf\x81;\xfb\x03s\xb3\xfe\xe0\xac\x1f=\x07f\x83\xc1/\xe7\xee\xa6\xfd\xf8K\xf8C\x7f\xf2\xfd\x8f3\x16\xde\xe6\xdc\x1d\x14\xcd[\x85\xc1v\xf9\\\x974\xd8\xd15\xd6\xf7\x04\x9e` x\xceuB\xb1\x81\xae}+\xab.>\xb7\xfc\x00\xa7&.\xbb!\x89c&KZ\xf1,\x1b\x8b\xeb\x12I\xac\x02\x1a\x92\xc7\xb4\x89\t\x1e\x1d\x1d\xacY`~\x1d\xab\xa3#\xc64w\r\xd6\xdd\x90\xeanK\xee\xee\xca\xe8\xb6R|\x13Wn\x07f\xe7\x02\xc1\xf9\xbf\x1d@n\xce\x7fK\xfe\xe9\xbf"\x1f|\x9b\xf8\xd7q\xec\xc2{\xf4\x85s\xf4{\xc3Yw\xba\xf3\xe6m\x92\xf9.\xcb\xc4\xe0\x93x\xc0\x90k7\nv\xb1\r\xfbDM\x18Ue\xb8\xa0\x05\x93\xd7\x92\xc2s\xb2\xf3;)B\x07[\xd0\xab(pd3zT\x02P\x8d\xf7\x18\x98}\xe5L\x97\x1e?\xd2.tU\xa7{\xea\t=\xad\x19\xdd\xa6\x94A\'\xc3i\x8e\xeev\x91n}}\x0e]\x8f\x02\xc1\xb9G\x07z\xf3\xdb\xf7\x18?\xffw\xdc_\x1f\xe2\x7f\x9aI\xfe\xfe:\xfb\xbbK\xcc{g\xd9\x0b\xa3\xb9\xf7O\xf3\xef@]\x13#O\xe3\tL\xfb\x8d\x02\xed\xe1\xcdl\xcdvnU\xb8\xb02\x9c\xdb\x9e,hKaw\xe2y\xa0\xa8F\xe3\x95E\x87\xe54\x87\x8c\x08)q\x88>\xd3\xa9\x033\x1d\x03U&#\xb5)\xdd-\xc9pS\x9c\xb3#\x11q\xc4\xba\xe08w7n|\xf2B08\x9d\x9b\x9b\x1b\x15\x15UZZ\xfa\xeeW\xd7\xd3~\xfa\xf7\xfd?\xff[\xc4\xc3\xa9\x88\x87\x13\xe9\xf7? ,\x9c\xcb\xb8w&\xfd\xfe\xdb |\xf5\x93\xef<\x8d\x07\xc8\xf9\x9e\x13\xaa7\x85uI\x85U\x07\x04V\x92\xae5I\xe0f\xe7;\xd9 ?\xb3\xfa\x15\nHD\x1b)\x95!\nro\t}\xb8.\x0b6`\x87L\\\xb8:u\xa0\x93\xdc\xd7\x95\x89\xb4\'\x8d\xf42aG\xf4\xc8\x10\xc9}<\xde9\x8c\xbd>q\x1a\x87[\xac*c\xe2\x13\x08\xf3w\x0f\xfc\xf2\x1f)?\x07\x0f>\xf4R\x7f\xbcIY\x18%\x7f7\xca\xfc\xfe"\xe1\xde\xd9\x96\xa9\xf7\xe7\x9e\xc6\x13\x98\xfb\xf2\xa3\xcf\x0bwrt\xdby\x95\xfb\x04\xe5\xfb8M\xf1<S\x1a\xa7+\x93\xd5E\xa1\x83]\x18,\xa1\xdb\xc1\xf6J\x96\xd1\xad\xc9\x04\x8b\x05R\x8cq\x1b1\xee\xea\x14\xb8!\tj\x8eG\xda\x0fu;\x12`(\xca\xe9\x89\x80\x06\xc2\xed\xc3\x11\xdd\x97h\x9f\xdc:=335\xd0\xdf\x0f m\xad0\xee\xff\xe9?\xf7<\x9c=\xf0\xc0\x17\xf7\xc3\r\xdc\xbd\xd1\xcc\xfbg\xf0\x0bg2\xef\x9f\xad\xf7^\xf2?\x1d\xaf@\xd0?\x15\xe8,\xa8-;(\xab\xd8\xc7\xef\xcaT7\'\n\xcdDq\x17\x99ger=\xf2\x1cHL\x1d,\x96\xba\x0b\xa9n\x1d\xdeSFu\x97aFLt\xb8*a\xd0J\xea\xb5\xe0\x9c\xa6\x98\xe3\x1e<\xec\x8c\x1c<\x8d\xb7\x0cD\xc0\xa3\xb1\xf0e\x9c\xfd\n\xe5\xf3\x99\xd1@p\xc6PU\r \xed\xb9v\x1d\xf3\xd3|\xc4\x03/\xee\xe1\x18\xe3\xfe\x05\xd2\xc2\x19\xce\xf7\x17\x89\x0b\xa3\xcd\xbew\x03\xcb\xc5k.\x18<\x01\x0f\x95\xec\x93\x94\xbc\xc5i\x88\x93\xb4$\nMX~\'\x91ma\xb0aq6$\xa6\xb8\x14LW!\x11Q\xe3<z\xa2\xa7\x1c\xd3[\x9f\x89\x16\x84`Zu\xa6B]\x07=\xced\x08\x89\xe8\x19I\x82N\xc6X\xcf\x1cp^\xc5\xb5}\x82\xb7\xdc<\xfc\xd1\xdc\xc7\xef~}\x03\xe0y%//\xe1\xc1t\xd4\x03/\xe6\x87/Iw\xcf\x81\x90\xd1\x16FI\x0b\xe7\x1b}\x97\x97\xe5OSS\x13\x18E\xfcs\xe2\x91= \x05\xf1\x1a\xe3Y\xed\xe9\\\x0b\x8d\xd7N\xa4\xd4\x93\xd0\x9d#~\xffv[^\xbaKG0\xab\xd0\x8dI\xcc\xde\xd7\xe1\xa3\xa9Ps\x82\xad9\xcem\x8fq;\x93\xf3\n\xd0\x92O\xdf\xf0\x17\xdb\xf9\xa8\x8e+\x89\r_P\xca\xc7\x0br\x82\x1e\xe7\xdd\xd9\x15\xbb\xd0"d\xcf\xd5SQ\x0f\'\xf0\xdf]%\xdf\x1b\xc5\xdf=K\xbd?\x9a\xb1p\xb6n\xf2\xe2\xb2x\x06\x07\x07\xc1\x10j\x0c\xae\xeaP\x96\x85Z\xd4\x8a\xe59\xf9\x8a.6\x1f\xecO\xbb\x15\xb2WW\xbe\xb8\xfe\xd5\x97\xed\x87q\xbde\xf4\x91:\xe1\xae-\x7f\x02\xc6\x96\xf2\xc4\x01\x1b\xb9\xdbB@\xacq\x83\xbd\xd4r#\xfaP\xa9f\xa7\xedB"\xf4\x19\xe7\xe8\x17\xec\x9a\x99\x1a\xce\x9d\x13\x84\xf9\x89\x10\xb1\xd7g3\xd3\xee}$}\xf0\x1e\x7f\xe1<\xf5\xde(\xff\xbb\x0b\x94{g\x9a\xa7\x96\x8f\xd7\x87\x1f~\x08\x86\xecX\xbb\xa91\x91\xe7\xe1i\xacD\x91++\xcf\xc1\xcf\xee S\xecB\x1av\x0f\xfa\xee\xad9i\xb0\x06l9qL\x0cZ-\xd4\xab#\x91\xd6xG[\x9c\xcb\x1e\x05;bM6tg\x91B|\xcd\xf2Nt\xc7\xd5\xa4\xda/h\xc5cE\xdc;\x9e\xc8/\xd07]\xb9\x7f\x078G\x9fo!\xdc?C\x00L^8C@)}\xf6\xe8\xe4\xc5e\xf1\xf8|\xbe\xd0[\xd4%0<\xfc"\x0bI\xd0\'\xcfGDR\x07\x8fw\xea\x88R\x96\x82\xae\xdaU\xd9I`7\xd1k\xa4+yh5\xa5\x95\xec\x1d\xb0\xe1<\x96\xd4n8\xf6\xd4\t*\xd4\xb7\x7f\xe3\x96\x15+^\n\xb3\x8c\xc6A\x9f\x91\x1b?\xa74M\xe9\x15\xfe\xc6\x8cs\x15h|\x87\x8d+6\xaf]K\x8dg/\xbc\xcdZ\x18\xceZ\x18V\xdc\x1f\xe6\xdfv\xb5O\x9eX6^@\xf8<\x1eJ\x80\xa8\x8c\x0e<\x07l\xbe:\xe9,3\x8b\xdbF#CrF19\x11\\R1\x13\xc0\x86\xcbY\x96iT\xa0E \x1b\xb7\x19dfG{\xb4\x1b\x8a\xf6\xb8\x12]\xc7\x0e\x12\x18kP\xd8\xf0.\xcb\xd54P\x80\x19\xaf\x0bt\x93\x1a\xacM\x08\x94\xb4\xcf\x8c\tVt\xc7\x87\x1f\xd1d\x05\xbb$\xf3f\xf9\xbcE\x14\xec0\x8d\xf5\x83\xc5nY<\xcd\x8d\x8d\xc0>\xf7`\xbc\x13\xd4<T\x06,\x14w2XV!\xb3\xa7H\xd8\xc8\xc5\xa3\xec\x8a\xddq\xdc\xc8?\xd9\x92k-As\xdd\xfe\x9d\xaf\xb8\xdbS\xbami\x88-\xba\x1bIE\xfa\x0e\x1e\xd6\xa3AQ5\xbei\xbb\x9a\xda\xf6QF\xcb\rQ\xc5D~\x82\x01\xfd\xe2!\x1ao\x90\xf9L\xabv\xbd\xb1\x01\xb3[4\xd3.\x9a\xeb\x94\xcd\x9b%s\x1d\xe6\x89\xfe\xd9\xc0\xf2x\x86\x87\x86\xd0\x17\xd9\xbd\xafW\x9acep ~\x96\x85\xcd\x84\xa5\xcc\x1e\xad\xc8,"\x81K\xdb\xd6\xbe\xdcSJ\xee7r\x1cz\xec\xd6\r(\xa5{L\x8ca\x17\xa3\x0fN\xee\xefMw\rD\xd5\xb6\xa3a\x15\x16nr\xbe\x8f5}\x90\xd2uSRs\x9d\xff\x16a\xfb\xaa-\xab\x94\xber\xed=[\x9aS\x8a\x16\'\xfd\n\xf9\x1ds\xfe\x1d\xabx\xde\xd49y\xfcY\xfe\xf9\xe8\x83\x0f\x80\xf1\xae5\xaf\x9b\xe9l\x0b\x8dac\xb2m<\xa6]D\x82\xe4dDN\x89\xdf\xb1\x01\\\xedP$"\xda\x0cWI:)\x11\xddL\x95\xe4F\xf5td\x0e@\xd8\xb3#\xd9pwL\xbb\r\x9db1\xc9/\xdb\xceGv\\\x89o\xf8\x14W\xf9\t\xfa\x15e?\x7f\x8fz\xa2P=\xa5\xcf\x19;\xb2:r\xd3\xeb\xb1[\x05SM\x92\xf9N\x80\xa7c\x0c\xf8g\x19\xfe\x04\x02\x01\xdf\xe4\xe4\xca\x17_\x04\xc3!\xb1\xcc\xccd\x1d+(\xecQH\x1d2\xfapy.$\xa7\xe4\xe1\xd0\x0f\xb7\xf5\xb2\xe4\x81J\xb6\xe7\x08\xce C\xa3\x90\x1a\xbd\xb1\xdfL\xf6t`F\xba9\xbd\x1e\xcc\xc9S\xf4\xb5o\xa0w\xe8y\x87d\xbd\x82\xb1~%,9\x8f\x16\xcc\x84\n\x8caR]\xe5/7xu\x02w\x16\xd0P`\xc1\x91om\x8a@\x8b}bh\xf6\xd1~p\x19H33\xc9{\xd1\x89S\x96\x9a\xdeIeXY\x1cg6\x03\xfd\x1e(\'9d\x14M&Zg\x16Q\x0e\xc0j\x9c\xab4\xbd<g\xf1;O\xa1x\x17\xdc\x1a\xef\xeaJE\xa0\x18\x18\t\x8f\x8e{\x19\xc5s\x9e\x00\xbd\x9ff\xfe\x84U\xd4\x8f\x05]V\'N;^\xa4\xf7\xaa\xf5\x93\x1a\xed\xad\xa2?\xc7nX\xbd\xfb\xb5\xa2\xebE\xeaI\xad\xe3\xa6\xc3\x1f\\~~\x81\xcaNLF\xdd\xab\xa11Lb\x99\xfd\xf0agQ\x0e\xa4\x91\xf4V*mE\xd9\xedJ\xb4\xaa\x17dD\x1do8\x0cW\xf1\xec\xd5\xe8k\xc6Gn]\xfd\xeaJ\xb9 \n\xe9\xcar9\x18]\x9d\xcc\x95+_\xd8\xb6}\xd5\xf1\x0b\xa2\x9e\xf3\x82\x13\x9fi5\x9d\xa8\x7fd}\xb4R\x9f\xae~\xceX\xe2\xd3V\xf8K\xd8\x1e\x06P\xd2\xad4\xc3\x94\xd6=\x86,\x1b\xaf\x90\x8c<\xca\xd2\xa5\xc5%\xb3>\x9f\x7fz\xda?\xe5\x9d\xf1M\x06f\xa6\xa6}\x13\xdf\xdc\xbc\x0e.a\xb1\x98\xd9i\xef\xf4\xd4\xf8\x94w|\xed\xda\xd7ssd\x97.\x8eFGG=^\x12CN\x8b?89\xe3\x1f\x9f\rx\xeb\x9bjQ\xaf\x9e\x97\x96\xf8TU\xb3G\x80\x7fJ\xa6t\xea[\x85[\xd3\xb6\xbe\xb2uU\xe1\xe7\x05\xd0\r\xc7\xb3\xe6\x17\x90O?\xfd\x14\x0c?t\xe8P`\xb9\x98\xe2p\xe8\xca5>>\x1e\xeaJ\xa5\xd2m\xdb\xb6\xf9\xfd\xfe[\xb7n\x99L&p5!!\xc1l6\xcf\xcc\xcc,\r\x01U\x19\x18R\x0c\x1c5\xa1\xd4yU\xba\xc9\xa2\x12\x9fA\xefS3{\xd0o8\x84f\xfc#<\xcf\xf4\x0f\xb8\xd5\xbau\xeb\x80\xe5\x8d\x1b7\x9ee\xf3\x8f\x8aw\xde\xd78Ug\x98\xd0\x1ag\xcbK\xbd\xda\xda`u\xd9TI\xf1\x94\xa6b\xb6\x14\xd0\xdb5\xe6z\x16\x9fC"\x97\xcb\x01\x9e\x0b\x17.\xfc\xb3\xf0L\x06\'\xaa\xc6\xcbt\x93*\x83W\x0b(\xad\xf3\xa9\xc0\xa1\xf5*\xf5\xbe"\x83O\xed\xf8\xda\xf68\x1e\xe0\x90U\xabV-\xb3\xa1\xfa{\x01\xb1\x00\xc6\xd7\xae]C\xd9\xae\xd1\xfcCx\xa6n\xfbj\xbd\x80\xc9\x80\xcf\xf5\x06\xaf\xba\xcc_\x0c\x80\x95N\xeb\x8d\xc1\xaab\xaf\x1a\xb9\xe5|\xc2?\x12\x89\xe4\xb9xB\xb4\x01T\x01%:\xe0\xcc\xe3\x0cy\xaex\xe7&+\xc7K\x80gJ}\x86b\xaf\n`\xd0O\x14\x15O\xa9K\xa7\x8a\x8b\'\xd5\xb6\xeb\xd0\xeco\x85\xeb\x9f/\xde\xb9\xf1\xea\xa92\x95\xb7@?\r\xf2\x8f\xb2b\xa6\x18\xf0Y\xe3-\xd4O\x81x\x159o"\x7f4\x9e\xf9\xc9\xda)\xa3\xcaw\xd8\xe0\xd7\xea|\xca\xea@\xb9aZ\xad\xf2\x15\x18f\xd5j\xdfa\xe4\x1b\xd7\xcc\x1f\x8bg"8V9Q\xaa\xf7j\x0c\x8f\x8eb\xafF7\xa9\xd4{\x95\x064]\xab\xa0\xaf\xe0\x19\x7fp\xe2\x0f\x94[\x937N\xde\x18\x1e\xfaz\xe8\xe4\xd8\xc9\x91\x1b\xc3\'n\x8d\x0c\xdf\x18:qk\xf8\xd4\xd8\xc9\xe1\x9b\xc7/\xdf\xbc\xe8\x0f\x04\xff\xe7\x91\x84\x85=\xf9\xff_\xf2\x7f+\xff\x0b\xf9!\xa0w'

decompressed_icon_data = zlib.decompress(compressed_icon_data)
